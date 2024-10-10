import os
import json

from src.database_connector.postgres_connector import PostgresConnector


class MatchInfoFetcher:

    @staticmethod
    def fetch_all_match_ids():
        postgres_connector = PostgresConnector()
        postgres_connector.open_connection_cursor("premier_league_stats")

        select_query = "select match_id from match_info"
        select_parameters = ()

        match_ids = []

        match_id_tuples = postgres_connector.execute_parameterized_select_query(select_query, select_parameters)
        for match in match_id_tuples:
            match_ids.append(match[0])

        return match_ids

os.environ['DB_PASS'] = "MySampleThing!#"
print(MatchInfoFetcher.fetch_all_match_ids())