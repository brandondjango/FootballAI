import os
import concurrent.futures

from src.data_processing.elevens_profiles.elevens_builder import ElevensBuilderUtil
from src.database_connector.postgres_connector import PostgresConnector


def get_matches_from_competition(competition_id: str, season: str):
    postgres_connector = PostgresConnector()
    postgres_connector.open_connection_cursor("premier_league_stats")

    select_query = "select match_id from match_info where competition_id = (%s) and season = (%s)"
    select_parameters = (competition_id, season)

    matches = postgres_connector.execute_parameterized_select_query(select_query, select_parameters)
    matches_to_return = []
    for match in matches:
        matches_to_return.append(match[0])
    return matches_to_return

def save_match_elevens(match: str):
    try:
        ElevensBuilderUtil.save_match_elevens(match)
        print("Saved match: " + match)
    except Exception as e:
        print(str(e))


os.environ['DB_PASS'] = "MySampleThing!#"
matches = get_matches_from_competition("9", "2023-2024")


with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
    # Submit tasks to scrape each URL and write to the database
    futures = [executor.submit(save_match_elevens, match) for match in matches]

    # Wait for all tasks to complete
for future in concurrent.futures.as_completed(futures):
    try:
        future.result()
    except Exception as e:
        print("Error in parallel: " + str(e))


