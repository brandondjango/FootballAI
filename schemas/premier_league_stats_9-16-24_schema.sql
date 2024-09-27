--
-- PostgreSQL database dump
--

-- Dumped from database version 14.13 (Homebrew)
-- Dumped by pg_dump version 14.13 (Homebrew)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: match_imported_status; Type: TABLE; Schema: public; Owner: brandon.lockridge
--

CREATE TABLE public.match_imported_status (
    match_id character varying(25) NOT NULL,
    match_imported boolean NOT NULL
);


ALTER TABLE public.match_imported_status OWNER TO "brandon.lockridge";

--
-- Name: match_info; Type: TABLE; Schema: public; Owner: brandon.lockridge
--

CREATE TABLE public.match_info (
    match_id character varying(25) NOT NULL,
    date character varying(25),
    competition_id character varying(25),
    season character varying(25),
    home_team character varying(100),
    away_team character varying(100),
    home_score integer,
    away_score integer
);


ALTER TABLE public.match_info OWNER TO "brandon.lockridge";

--
-- Name: match_shots_stats; Type: TABLE; Schema: public; Owner: brandon.lockridge
--

CREATE TABLE public.match_shots_stats (
    minute character varying(10),
    player character varying(100),
    team character varying(50),
    xg_shot character varying(10),
    psxg_shot character varying(10),
    outcome character varying(50),
    distance character varying(20),
    body_part character varying(50),
    notes character varying(100),
    sca_1_player character varying(100),
    sca_1_type character varying(100),
    sca_2_player character varying(100),
    sca_2_type character varying(100),
    match_id character varying(20),
    shot_id character varying(128) NOT NULL,
    player_id character varying(100),
    sca1_player_id character varying(100),
    sca2_player_id character varying(100)
);


ALTER TABLE public.match_shots_stats OWNER TO "brandon.lockridge";

--
-- Name: match_summary_stats; Type: TABLE; Schema: public; Owner: brandon.lockridge
--

CREATE TABLE public.match_summary_stats (
    match_id character varying(20),
    player_id character varying(20),
    player character varying(100),
    shirtnumber character varying(10),
    nationality character varying(20),
    "position" character varying(20),
    age character varying(10),
    minutes character varying(10),
    goals character varying(10),
    assists character varying(10),
    pens_made character varying(10),
    pens_att character varying(10),
    shots character varying(10),
    shots_on_target character varying(10),
    cards_yellow character varying(10),
    cards_red character varying(10),
    touches character varying(10),
    tackles character varying(10),
    interceptions character varying(10),
    blocks character varying(10),
    xg character varying(10),
    npxg character varying(10),
    xg_assist character varying(10),
    sca character varying(10),
    gca character varying(10),
    passes_completed character varying(10),
    passes character varying(10),
    passes_pct character varying(10),
    progressive_passes character varying(10),
    carries character varying(10),
    progressive_carries character varying(10),
    take_ons character varying(10),
    take_ons_won character varying(10),
    subbed_on character varying(10),
    subbed_off character varying(10)
);


ALTER TABLE public.match_summary_stats OWNER TO "brandon.lockridge";

--
-- Name: player_match_stats; Type: TABLE; Schema: public; Owner: brandon.lockridge
--

CREATE TABLE public.player_match_stats (
    match_id character varying(100)
);


ALTER TABLE public.player_match_stats OWNER TO "brandon.lockridge";

--
-- Name: players; Type: TABLE; Schema: public; Owner: brandon.lockridge
--

CREATE TABLE public.players (
    player_id character varying(100) NOT NULL,
    player_name character varying(100)
);


ALTER TABLE public.players OWNER TO "brandon.lockridge";

--
-- Name: match_imported_status match_imported_status_pkey; Type: CONSTRAINT; Schema: public; Owner: brandon.lockridge
--

ALTER TABLE ONLY public.match_imported_status
    ADD CONSTRAINT match_imported_status_pkey PRIMARY KEY (match_id);


--
-- Name: match_info match_info_pkey; Type: CONSTRAINT; Schema: public; Owner: brandon.lockridge
--

ALTER TABLE ONLY public.match_info
    ADD CONSTRAINT match_info_pkey PRIMARY KEY (match_id);


--
-- Name: match_shots_stats match_shots_stats_pkey; Type: CONSTRAINT; Schema: public; Owner: brandon.lockridge
--

ALTER TABLE ONLY public.match_shots_stats
    ADD CONSTRAINT match_shots_stats_pkey PRIMARY KEY (shot_id);


--
-- Name: players player_id_unique; Type: CONSTRAINT; Schema: public; Owner: brandon.lockridge
--

ALTER TABLE ONLY public.players
    ADD CONSTRAINT player_id_unique PRIMARY KEY (player_id);


--
-- Name: match_summary_stats unique_match_player_combination; Type: CONSTRAINT; Schema: public; Owner: brandon.lockridge
--

ALTER TABLE ONLY public.match_summary_stats
    ADD CONSTRAINT unique_match_player_combination UNIQUE (match_id, player_id);


--
-- Name: match_summary_stats unique_match_player_constraint; Type: CONSTRAINT; Schema: public; Owner: brandon.lockridge
--

ALTER TABLE ONLY public.match_summary_stats
    ADD CONSTRAINT unique_match_player_constraint UNIQUE (match_id, player_id);


--
-- Name: match_shots_stats unique_shot_id; Type: CONSTRAINT; Schema: public; Owner: brandon.lockridge
--

ALTER TABLE ONLY public.match_shots_stats
    ADD CONSTRAINT unique_shot_id UNIQUE (shot_id);


--
-- Name: players unique_varchar_id; Type: CONSTRAINT; Schema: public; Owner: brandon.lockridge
--

ALTER TABLE ONLY public.players
    ADD CONSTRAINT unique_varchar_id UNIQUE (player_id);


--
-- PostgreSQL database dump complete
--

