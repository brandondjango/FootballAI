import os

from src.database_connector.postgres_connector import PostgresConnector

#An eleven profile really has 10 outfield players.
#Subs accounted for
#red cards not accounted for
class ElevensBuilderUtil:

    @staticmethod
    def elevens_builder(match_id, postgres_connector=None):
        if(postgres_connector is None):
            postgres_connector = PostgresConnector()
            postgres_connector.open_connection_cursor("premier_league_stats")

        print(match_id)
        select_query = "select player_id, player, team_id, subbed_on, subbed_off from match_summary_stats where match_id = '" + match_id + "'"
        select_parameters = ()

        match_players = postgres_connector.execute_parameterized_select_query(select_query, select_parameters)

        initial_elevens_by_team_id = {}

        #split the players into their teams
        for player in match_players:
            team_id = player[2]
            if initial_elevens_by_team_id.get(team_id) is None:
                initial_elevens_by_team_id[team_id] = []
            initial_elevens_by_team_id[team_id].append(player)


        #store substituted players so we can build the varied 11s
        substitued_players = {}
        #store the players that were not subbed because we know they willl be in all the 11s we create from this match
        base_eleven_profile = {}
        #create elevens profiles for each team
        for team in initial_elevens_by_team_id.keys():
            base_eleven_profile[team] = []
            substitued_players[team] = []
            #build base team
            for player in initial_elevens_by_team_id[team]:
                minute_subbed_on = player[3]
                minute_subbed_off = player[4]
                if (minute_subbed_on is None) and (minute_subbed_off is None):
                    base_eleven_profile[team].append(player)
                else:
                    substitued_players[team].append(player)





os.environ['DB_PASS'] = "MySampleThing!#"
ElevensBuilderUtil.elevens_builder("5d4a5006")

