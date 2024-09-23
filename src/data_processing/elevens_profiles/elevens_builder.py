import os
import json

from src.database_connector.postgres_connector import PostgresConnector

#An eleven profile really has 10 outfield players.
#Subs accounted for
#red cards not accounted for
class ElevensBuilderUtil:

    @staticmethod
    def elevens_builder(match_id: str):
        #player_tuples
        match_players = ElevensBuilderUtil.get_match_players(match_id)
        #hash splitting player_tuples by team id
        initial_elevens_by_team_id = ElevensBuilderUtil.split_players_into_teams(match_players)


        #store substituted players so we can build the varied 11s
        subbed_on_players = {}
        subbed_off_players = {}
        #store the players that were not subbed because we know they willl be in all the 11s we create from this match
        base_eleven_profile = {}
        #discover subbed on players, subbed off, and players who played the whole game
        for team in initial_elevens_by_team_id.keys():
            base_eleven_profile[team] = []
            subbed_on_players[team] = []
            subbed_off_players[team] = []
            #build base team
            for player in initial_elevens_by_team_id[team]:
                minute_subbed_on = player[4]
                minute_subbed_off = player[3]
                #these if statements still cover the case where a palyer is subbed on and off
                if (minute_subbed_on is None) and (minute_subbed_off is None):
                    base_eleven_profile[team].append(player)
                elif (minute_subbed_off is not None):
                    subbed_off_players[team].append(player)
                elif (minute_subbed_on is not None):
                    subbed_on_players[team].append(player)


        #store when each 11 came onto the field
        minute_eleven_profile_went_on = {}

        #for both teams
        for team in base_eleven_profile.keys():
            #create elevens based on subbed on and off players
            elevens = {}

            #get starters that were subbed off
            starters = base_eleven_profile[team]
            for subbed_off_player in subbed_off_players[team]:
                if subbed_off_player[4] is None:
                    starters.append(subbed_off_player)

            #starters profile id
            starters_profile_id = ElevensBuilderUtil.id_for_player_touple(starters)

            #starters 11s profile
            elevens[starters_profile_id] = starters

            current_elevens = starters

            #account for group substititions so we don't create multiple 11s for substitutions of 2 or more
            grouped_subbed_on_players = ElevensBuilderUtil.group_subbed_on_players_by_minute(subbed_on_players[team])
            group_subbed_off_players = ElevensBuilderUtil.group_subbed_off_players_by_minute(subbed_off_players[team])


            #store starters
            minute_eleven_profile_went_on[starters_profile_id] = "0"
            for minute_of_subs in grouped_subbed_on_players.keys():
                current_subbed_on_group = grouped_subbed_on_players[minute_of_subs]
                current_subbed_off_group = group_subbed_off_players[minute_of_subs]


                for sub_off in current_subbed_off_group:
                    current_elevens.remove(sub_off)
                for sub_on in current_subbed_on_group:
                    current_elevens.append(sub_on)
                updated_elevens_id = ElevensBuilderUtil.id_for_player_touple(current_elevens)

                elevens[updated_elevens_id] = current_elevens
                minute_eleven_profile_went_on[updated_elevens_id] = minute_of_subs
            #Save the elevens profiles(once for each team
            ElevensBuilderUtil.save_elevens_profiles(elevens, minute_eleven_profile_went_on, team, match_id)







    #returns player_tuples in this order: player_id, player, team_id, subbed_off, subbed_on:
    @staticmethod
    def get_match_players(match_id: str):
        postgres_connector = PostgresConnector()
        postgres_connector.open_connection_cursor("premier_league_stats")

        select_query = "select player_id, player, team_id, subbed_off, subbed_on from match_summary_stats where match_id = '" + match_id + "'"
        select_parameters = ()

        match_players = postgres_connector.execute_parameterized_select_query(select_query, select_parameters)
        return match_players

    @staticmethod
    def split_players_into_teams(match_players):
        initial_elevens_by_team_id = {}
        #split the players into their teams
        for player in match_players:
            team_id = player[2]
            if initial_elevens_by_team_id.get(team_id) is None:
                initial_elevens_by_team_id[team_id] = []
            initial_elevens_by_team_id[team_id].append(player)
        return initial_elevens_by_team_id



    @staticmethod
    def order_player_ids_alphabetically(player_touples):
        sorted_player_tuples = sorted(player_touples, key=lambda x: x[0])
        return sorted_player_tuples

    @staticmethod
    def group_subbed_on_players_by_minute(player_touples):
        grouped_subs = {}
        for player in player_touples:
            key = player[-1]
            if key not in grouped_subs:
                grouped_subs[key] = []
            grouped_subs[key].append(player)
        return grouped_subs

    @staticmethod
    def group_subbed_off_players_by_minute(player_touples):
        grouped_subs = {}
        for player in player_touples:
            key = player[-2]
            if key not in grouped_subs:
                grouped_subs[key] = []
            grouped_subs[key].append(player)
        return grouped_subs


    @staticmethod
    def id_for_player_touple(player_touples):
        id_to_return = ""
        player_touples = ElevensBuilderUtil.order_player_ids_alphabetically(player_touples)
        for player_touple in player_touples:
            id_to_return = id_to_return + player_touple[0]
        return id_to_return

    @staticmethod
    def save_elevens_profiles(elevens: {}, minute_eleven_profile_went_on: {}, team_id: str, match_id: str):
        for elevens_id in elevens.keys():
            player_array = []
            for player_touple in elevens[elevens_id]:
                player_hash = {}
                player_hash["player_id"] = player_touple[0]
                player_hash["player_name"] = player_touple[1]
                player_array.append((player_hash))

            #print(elevens_id)
            json_player_array=json.dumps(player_array)
            #print(json_player_array)
            eleven_to_save = {}
            eleven_to_save["team_id"] = team_id
            eleven_to_save["elevens_id"] = elevens_id
            eleven_to_save["elevens_players"] = json_player_array
            eleven_to_save["match_id"] = match_id
            eleven_to_save["minute"] = minute_eleven_profile_went_on[elevens_id]

            ElevensBuilderUtil.insert_elevens_information_into_database(eleven_to_save)


    @staticmethod
    def insert_elevens_information_into_database(elevens_dict: {}):
        insert_query = ("INSERT INTO " +
                       "elevens_profiles(team_id, elevens_id, elevens_players,match_id,minutes)" +
                       " VALUES ((%s),(%s),(%s),(%s),(%s))")
        insert_parameters = (elevens_dict["team_id"],
                             elevens_dict["elevens_id"],
                             str(elevens_dict["elevens_players"]),
                             elevens_dict["match_id"],
                             elevens_dict["minute"])
        postgres_connector = PostgresConnector()
        postgres_connector.open_connection_cursor("premier_league_stats")
        postgres_connector.execute_parameterized_insert_query(insert_query, insert_parameters)



