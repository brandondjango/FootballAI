import os

from src.database_connector.postgres_connector import PostgresConnector


class SCAPlayerShotsUtil:

    @staticmethod
    def update_sca_player_ids(postgres_connector=None):
        if(postgres_connector is None):
            postgres_connector = PostgresConnector()
            postgres_connector.open_connection_cursor("premier_league_stats")

        select_query = "select sca_1_player, sca_2_player, shot_id  from match_shots_stats"
        select_parameters = ()

        all_match_shots = postgres_connector.execute_parameterized_select_query(select_query, select_parameters)

        error_shots = []
        for shot in all_match_shots:
            sca_player_1_name = shot[0]
            sca_player_2_name = shot[1]
            shot_id = shot[2]
            try:
                if sca_player_1_name != '':
                    get_sca_player_1_id_query = "select player_id from players where player_name = (%s)"
                    get_sca_player_1_id_parameters = (sca_player_1_name,)
                    sca_player_1_id = postgres_connector.execute_parameterized_select_query(get_sca_player_1_id_query, get_sca_player_1_id_parameters)[0]
                    update_sca_player_1_id_query = "UPDATE match_shots_stats SET sca1_player_id = (%s) WHERE sca_1_player = (%s);"
                    update_sca_player_1_id_parameters = (sca_player_1_id, sca_player_1_name)
                    print("Updating SCA1: " + str(update_sca_player_1_id_parameters))
                    postgres_connector.execute_parameterized_insert_query(update_sca_player_1_id_query, update_sca_player_1_id_parameters)
            except Exception as e:
                print("Error updating SCA1 id for player: " + sca_player_1_name)
                error_shots.append(shot_id)
            try:
                if sca_player_2_name != '':
                    get_sca_player_2_id_query = "select player_id from players where player_name = (%s)"
                    get_sca_player_2_id_parameters = (sca_player_2_name,)
                    sca_player_2_id = postgres_connector.execute_parameterized_select_query(get_sca_player_2_id_query, get_sca_player_2_id_parameters)[0]
                    update_sca_player_2_id_query = "UPDATE match_shots_stats SET sca2_player_id = (%s) WHERE sca_2_player = (%s);"
                    update_sca_player_2_id_parameters = (sca_player_2_id, sca_player_2_name)
                    postgres_connector.execute_parameterized_insert_query(update_sca_player_2_id_query, update_sca_player_2_id_parameters)
                    print("Updating SCA2: " + str(update_sca_player_2_id_parameters))
            except Exception as e:
                print("Error updating SCA2 id for player: " + sca_player_2_name)
                error_shots.append(shot_id)
        print("error shots: \n" + error_shots)


os.environ['DB_PASS'] = "MySampleThing!#"
SCAPlayerShotsUtil.update_sca_player_ids()



