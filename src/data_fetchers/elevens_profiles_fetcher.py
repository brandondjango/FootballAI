import os
import json

from src.database_connector.postgres_connector import PostgresConnector

#An eleven profile really has 10 outfield players.
#Subs accounted for
#red cards not accounted for
class ElevensProfileFetcher:

    @staticmethod
    def fetch_elevens_by_match_and_team_id_in_minutes_order(match_id: str, team_id: str):
        postgres_connector = PostgresConnector()
        postgres_connector.open_connection_cursor("premier_league_stats")

        select_query = "select elevens_id, minutes from elevens_profiles where match_id = %s and team_id = %s order by minutes"
        select_parameters = (match_id, team_id)

        elevens_for_match = postgres_connector.execute_parameterized_select_query(select_query, select_parameters)
        for eleven in elevens_for_match:
            print(eleven)
        return elevens_for_match



os.environ['DB_PASS'] = "MySampleThing!#"
ElevensProfileFetcher.fetch_elevens_by_match_and_team_id_in_minutes_order('56a137f7', "e297cd13")