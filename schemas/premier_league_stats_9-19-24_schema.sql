ALTER TABLE match_summary_stats
ADD COLUMN team_id VARCHAR(20);

CREATE TABLE elevens_profiles (
                                  team_id VARCHAR,
                                  elevens_id VARCHAR,
                                  elevens_players JSONB,  -- Field to store eleven players
                                  match_id VARCHAR,
                                  minutes VARCHAR
);