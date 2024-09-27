ALTER TABLE elevens_profile
    ADD CONSTRAINT unique_elevens_match_id
        UNIQUE (elevens_id, match_id);