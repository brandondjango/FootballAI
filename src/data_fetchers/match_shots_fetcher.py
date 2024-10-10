import os
import json

from src.database_connector.postgres_connector import PostgresConnector

#An eleven profile really has 10 outfield players.
#Subs accounted for
#red cards not accounted for
class MatchShotsFetcher:

    @staticmethod
    def fetch_shots_by_match_and_team_id_in_minutes_order(match_id: str):
        postgres_connector = PostgresConnector()
        postgres_connector.open_connection_cursor("premier_league_stats")

        select_query = "select shot_id, minute from match_shots_stats where match_id = %s order by minute"
        select_parameters = (match_id,)

        shots_for_match = postgres_connector.execute_parameterized_select_query(select_query, select_parameters)
        for shot in shots_for_match:
            print(shot)
        return shots_for_match



os.environ['DB_PASS'] = "MySampleThing!#"
MatchShotsFetcher.fetch_shots_by_match_and_team_id_in_minutes_order('56a137f7')