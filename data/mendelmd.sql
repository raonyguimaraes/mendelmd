--
-- PostgreSQL database dump
--

-- Dumped from database version 9.6.5
-- Dumped by pg_dump version 9.6.5

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: account_emailaddress; Type: TABLE; Schema: public; Owner: raony
--

CREATE TABLE account_emailaddress (
    id integer NOT NULL,
    email character varying(254) NOT NULL,
    verified boolean NOT NULL,
    "primary" boolean NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE account_emailaddress OWNER TO raony;

--
-- Name: account_emailaddress_id_seq; Type: SEQUENCE; Schema: public; Owner: raony
--

CREATE SEQUENCE account_emailaddress_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE account_emailaddress_id_seq OWNER TO raony;

--
-- Name: account_emailaddress_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: raony
--

ALTER SEQUENCE account_emailaddress_id_seq OWNED BY account_emailaddress.id;


--
-- Name: account_emailconfirmation; Type: TABLE; Schema: public; Owner: raony
--

CREATE TABLE account_emailconfirmation (
    id integer NOT NULL,
    created timestamp with time zone NOT NULL,
    sent timestamp with time zone,
    key character varying(64) NOT NULL,
    email_address_id integer NOT NULL
);


ALTER TABLE account_emailconfirmation OWNER TO raony;

--
-- Name: account_emailconfirmation_id_seq; Type: SEQUENCE; Schema: public; Owner: raony
--

CREATE SEQUENCE account_emailconfirmation_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE account_emailconfirmation_id_seq OWNER TO raony;

--
-- Name: account_emailconfirmation_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: raony
--

ALTER SEQUENCE account_emailconfirmation_id_seq OWNED BY account_emailconfirmation.id;


--
-- Name: auth_group; Type: TABLE; Schema: public; Owner: raony
--

CREATE TABLE auth_group (
    id integer NOT NULL,
    name character varying(80) NOT NULL
);


ALTER TABLE auth_group OWNER TO raony;

--
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: raony
--

CREATE SEQUENCE auth_group_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE auth_group_id_seq OWNER TO raony;

--
-- Name: auth_group_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: raony
--

ALTER SEQUENCE auth_group_id_seq OWNED BY auth_group.id;


--
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: raony
--

CREATE TABLE auth_group_permissions (
    id integer NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE auth_group_permissions OWNER TO raony;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: raony
--

CREATE SEQUENCE auth_group_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE auth_group_permissions_id_seq OWNER TO raony;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: raony
--

ALTER SEQUENCE auth_group_permissions_id_seq OWNED BY auth_group_permissions.id;


--
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: raony
--

CREATE TABLE auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


ALTER TABLE auth_permission OWNER TO raony;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: raony
--

CREATE SEQUENCE auth_permission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE auth_permission_id_seq OWNER TO raony;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: raony
--

ALTER SEQUENCE auth_permission_id_seq OWNED BY auth_permission.id;


--
-- Name: auth_user; Type: TABLE; Schema: public; Owner: raony
--

CREATE TABLE auth_user (
    id integer NOT NULL,
    password character varying(128) NOT NULL,
    last_login timestamp with time zone,
    is_superuser boolean NOT NULL,
    username character varying(150) NOT NULL,
    first_name character varying(30) NOT NULL,
    last_name character varying(30) NOT NULL,
    email character varying(254) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL
);


ALTER TABLE auth_user OWNER TO raony;

--
-- Name: auth_user_groups; Type: TABLE; Schema: public; Owner: raony
--

CREATE TABLE auth_user_groups (
    id integer NOT NULL,
    user_id integer NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE auth_user_groups OWNER TO raony;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: raony
--

CREATE SEQUENCE auth_user_groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE auth_user_groups_id_seq OWNER TO raony;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: raony
--

ALTER SEQUENCE auth_user_groups_id_seq OWNED BY auth_user_groups.id;


--
-- Name: auth_user_id_seq; Type: SEQUENCE; Schema: public; Owner: raony
--

CREATE SEQUENCE auth_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE auth_user_id_seq OWNER TO raony;

--
-- Name: auth_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: raony
--

ALTER SEQUENCE auth_user_id_seq OWNED BY auth_user.id;


--
-- Name: auth_user_user_permissions; Type: TABLE; Schema: public; Owner: raony
--

CREATE TABLE auth_user_user_permissions (
    id integer NOT NULL,
    user_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE auth_user_user_permissions OWNER TO raony;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: raony
--

CREATE SEQUENCE auth_user_user_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE auth_user_user_permissions_id_seq OWNER TO raony;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: raony
--

ALTER SEQUENCE auth_user_user_permissions_id_seq OWNED BY auth_user_user_permissions.id;


--
-- Name: cases_case; Type: TABLE; Schema: public; Owner: raony
--

CREATE TABLE cases_case (
    id integer NOT NULL,
    status character varying(100) NOT NULL,
    name character varying(600) NOT NULL,
    description text,
    father_id integer,
    mother_id integer,
    user_id integer NOT NULL
);


ALTER TABLE cases_case OWNER TO raony;

--
-- Name: cases_case_case_groups; Type: TABLE; Schema: public; Owner: raony
--

CREATE TABLE cases_case_case_groups (
    id integer NOT NULL,
    case_id integer NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE cases_case_case_groups OWNER TO raony;

--
-- Name: cases_case_case_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: raony
--

CREATE SEQUENCE cases_case_case_groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE cases_case_case_groups_id_seq OWNER TO raony;

--
-- Name: cases_case_case_groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: raony
--

ALTER SEQUENCE cases_case_case_groups_id_seq OWNED BY cases_case_case_groups.id;


--
-- Name: cases_case_cases; Type: TABLE; Schema: public; Owner: raony
--

CREATE TABLE cases_case_cases (
    id integer NOT NULL,
    case_id integer NOT NULL,
    individual_id integer NOT NULL
);


ALTER TABLE cases_case_cases OWNER TO raony;

--
-- Name: cases_case_cases_id_seq; Type: SEQUENCE; Schema: public; Owner: raony
--

CREATE SEQUENCE cases_case_cases_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE cases_case_cases_id_seq OWNER TO raony;

--
-- Name: cases_case_cases_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: raony
--

ALTER SEQUENCE cases_case_cases_id_seq OWNED BY cases_case_cases.id;


--
-- Name: cases_case_children; Type: TABLE; Schema: public; Owner: raony
--

CREATE TABLE cases_case_children (
    id integer NOT NULL,
    case_id integer NOT NULL,
    individual_id integer NOT NULL
);


ALTER TABLE cases_case_children OWNER TO raony;

--
-- Name: cases_case_children_id_seq; Type: SEQUENCE; Schema: public; Owner: raony
--

CREATE SEQUENCE cases_case_children_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE cases_case_children_id_seq OWNER TO raony;

--
-- Name: cases_case_children_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: raony
--

ALTER SEQUENCE cases_case_children_id_seq OWNED BY cases_case_children.id;


--
-- Name: cases_case_control_groups; Type: TABLE; Schema: public; Owner: raony
--

CREATE TABLE cases_case_control_groups (
    id integer NOT NULL,
    case_id integer NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE cases_case_control_groups OWNER TO raony;

--
-- Name: cases_case_control_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: raony
--

CREATE SEQUENCE cases_case_control_groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE cases_case_control_groups_id_seq OWNER TO raony;

--
-- Name: cases_case_control_groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: raony
--

ALTER SEQUENCE cases_case_control_groups_id_seq OWNED BY cases_case_control_groups.id;


--
-- Name: cases_case_controls; Type: TABLE; Schema: public; Owner: raony
--

CREATE TABLE cases_case_controls (
    id integer NOT NULL,
    case_id integer NOT NULL,
    individual_id integer NOT NULL
);


ALTER TABLE cases_case_controls OWNER TO raony;

--
-- Name: cases_case_controls_id_seq; Type: SEQUENCE; Schema: public; Owner: raony
--

CREATE SEQUENCE cases_case_controls_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE cases_case_controls_id_seq OWNER TO raony;

--
-- Name: cases_case_controls_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: raony
--

ALTER SEQUENCE cases_case_controls_id_seq OWNED BY cases_case_controls.id;


--
-- Name: cases_case_id_seq; Type: SEQUENCE; Schema: public; Owner: raony
--

CREATE SEQUENCE cases_case_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE cases_case_id_seq OWNER TO raony;

--
-- Name: cases_case_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: raony
--

ALTER SEQUENCE cases_case_id_seq OWNED BY cases_case.id;


--
-- Name: cases_case_shared_with_groups; Type: TABLE; Schema: public; Owner: raony
--

CREATE TABLE cases_case_shared_with_groups (
    id integer NOT NULL,
    case_id integer NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE cases_case_shared_with_groups OWNER TO raony;

--
-- Name: cases_case_shared_with_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: raony
--

CREATE SEQUENCE cases_case_shared_with_groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE cases_case_shared_with_groups_id_seq OWNER TO raony;

--
-- Name: cases_case_shared_with_groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: raony
--

ALTER SEQUENCE cases_case_shared_with_groups_id_seq OWNED BY cases_case_shared_with_groups.id;


--
-- Name: cases_case_shared_with_users; Type: TABLE; Schema: public; Owner: raony
--

CREATE TABLE cases_case_shared_with_users (
    id integer NOT NULL,
    case_id integer NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE cases_case_shared_with_users OWNER TO raony;

--
-- Name: cases_case_shared_with_users_id_seq; Type: SEQUENCE; Schema: public; Owner: raony
--

CREATE SEQUENCE cases_case_shared_with_users_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE cases_case_shared_with_users_id_seq OWNER TO raony;

--
-- Name: cases_case_shared_with_users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: raony
--

ALTER SEQUENCE cases_case_shared_with_users_id_seq OWNED BY cases_case_shared_with_users.id;


--
-- Name: celery_taskmeta; Type: TABLE; Schema: public; Owner: raony
--

CREATE TABLE celery_taskmeta (
    id integer NOT NULL,
    task_id character varying(255) NOT NULL,
    status character varying(50) NOT NULL,
    result text,
    date_done timestamp with time zone NOT NULL,
    traceback text,
    hidden boolean NOT NULL,
    meta text
);


ALTER TABLE celery_taskmeta OWNER TO raony;

--
-- Name: celery_taskmeta_id_seq; Type: SEQUENCE; Schema: public; Owner: raony
--

CREATE SEQUENCE celery_taskmeta_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE celery_taskmeta_id_seq OWNER TO raony;

--
-- Name: celery_taskmeta_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: raony
--

ALTER SEQUENCE celery_taskmeta_id_seq OWNED BY celery_taskmeta.id;


--
-- Name: celery_tasksetmeta; Type: TABLE; Schema: public; Owner: raony
--

CREATE TABLE celery_tasksetmeta (
    id integer NOT NULL,
    taskset_id character varying(255) NOT NULL,
    result text NOT NULL,
    date_done timestamp with time zone NOT NULL,
    hidden boolean NOT NULL
);


ALTER TABLE celery_tasksetmeta OWNER TO raony;

--
-- Name: celery_tasksetmeta_id_seq; Type: SEQUENCE; Schema: public; Owner: raony
--

CREATE SEQUENCE celery_tasksetmeta_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE celery_tasksetmeta_id_seq OWNER TO raony;

--
-- Name: celery_tasksetmeta_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: raony
--

ALTER SEQUENCE celery_tasksetmeta_id_seq OWNED BY celery_tasksetmeta.id;


--
-- Name: diseases_disease; Type: TABLE; Schema: public; Owner: raony
--

CREATE TABLE diseases_disease (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    omim_id character varying(255) NOT NULL,
    chr_location character varying(255) NOT NULL,
    gene_names character varying(255) NOT NULL
);


ALTER TABLE diseases_disease OWNER TO raony;

--
-- Name: diseases_disease_id_seq; Type: SEQUENCE; Schema: public; Owner: raony
--

CREATE SEQUENCE diseases_disease_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE diseases_disease_id_seq OWNER TO raony;

--
-- Name: diseases_disease_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: raony
--

ALTER SEQUENCE diseases_disease_id_seq OWNED BY diseases_disease.id;


--
-- Name: diseases_gene; Type: TABLE; Schema: public; Owner: raony
--

CREATE TABLE diseases_gene (
    id integer NOT NULL,
    official_name character varying(255) NOT NULL,
    chromossome character varying(255),
    names text,
    strand character varying(255),
    chr_location character varying(255),
    transcription_start integer,
    transcription_end integer,
    cds_start integer,
    cds_end integer,
    exons_count character varying(500),
    exons_start text,
    exons_end text
);


ALTER TABLE diseases_gene OWNER TO raony;

--
-- Name: diseases_gene_diseases; Type: TABLE; Schema: public; Owner: raony
--

CREATE TABLE diseases_gene_diseases (
    id integer NOT NULL,
    gene_id integer NOT NULL,
    disease_id integer NOT NULL
);


ALTER TABLE diseases_gene_diseases OWNER TO raony;

--
-- Name: diseases_gene_diseases_id_seq; Type: SEQUENCE; Schema: public; Owner: raony
--

CREATE SEQUENCE diseases_gene_diseases_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE diseases_gene_diseases_id_seq OWNER TO raony;

--
-- Name: diseases_gene_diseases_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: raony
--

ALTER SEQUENCE diseases_gene_diseases_id_seq OWNED BY diseases_gene_diseases.id;


--
-- Name: diseases_gene_id_seq; Type: SEQUENCE; Schema: public; Owner: raony
--

CREATE SEQUENCE diseases_gene_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE diseases_gene_id_seq OWNER TO raony;

--
-- Name: diseases_gene_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: raony
--

ALTER SEQUENCE diseases_gene_id_seq OWNED BY diseases_gene.id;


--
-- Name: diseases_hgmdgene; Type: TABLE; Schema: public; Owner: raony
--

CREATE TABLE diseases_hgmdgene (
    id integer NOT NULL,
    symbol character varying(255) NOT NULL,
    aliases text,
    description text,
    description_aliases text,
    location character varying(255) NOT NULL,
    n_mutations integer
);


ALTER TABLE diseases_hgmdgene OWNER TO raony;

--
-- Name: diseases_hgmdgene_diseases; Type: TABLE; Schema: public; Owner: raony
--

CREATE TABLE diseases_hgmdgene_diseases (
    id integer NOT NULL,
    hgmdgene_id integer NOT NULL,
    hgmdphenotype_id integer NOT NULL
);


ALTER TABLE diseases_hgmdgene_diseases OWNER TO raony;

--
-- Name: diseases_hgmdgene_diseases_id_seq; Type: SEQUENCE; Schema: public; Owner: raony
--

CREATE SEQUENCE diseases_hgmdgene_diseases_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE diseases_hgmdgene_diseases_id_seq OWNER TO raony;

--
-- Name: diseases_hgmdgene_diseases_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: raony
--

ALTER SEQUENCE diseases_hgmdgene_diseases_id_seq OWNED BY diseases_hgmdgene_diseases.id;


--
-- Name: diseases_hgmdgene_id_seq; Type: SEQUENCE; Schema: public; Owner: raony
--

CREATE SEQUENCE diseases_hgmdgene_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE diseases_hgmdgene_id_seq OWNER TO raony;

--
-- Name: diseases_hgmdgene_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: raony
--

ALTER SEQUENCE diseases_hgmdgene_id_seq OWNED BY diseases_hgmdgene.id;


--
-- Name: diseases_hgmdmutation; Type: TABLE; Schema: public; Owner: raony
--

CREATE TABLE diseases_hgmdmutation (
    id integer NOT NULL,
    mutation_type character varying(255),
    acession character varying(255),
    reference text,
    extras text,
    rsid character varying(255),
    dm_mutation boolean NOT NULL,
    coordinate character varying(100),
    chromossome character varying(100),
    "position" character varying(100),
    codon_change character varying(255),
    aa_change character varying(255),
    hgvs_nucleotide character varying(100),
    hgvs_protein character varying(100),
    splicing_mutation character varying(255),
    regulatory_sequence text,
    deletion_sequence text,
    insertion_sequence text,
    dna_level character varying(255),
    description character varying(255),
    insertion_duplication character varying(255),
    amplified_sequence character varying(255),
    location character varying(255),
    normal_range character varying(255),
    pathological_range character varying(255),
    gene_id integer NOT NULL,
    phenotype_id integer NOT NULL
);


ALTER TABLE diseases_hgmdmutation OWNER TO raony;

--
-- Name: diseases_hgmdmutation_id_seq; Type: SEQUENCE; Schema: public; Owner: raony
--

CREATE SEQUENCE diseases_hgmdmutation_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE diseases_hgmdmutation_id_seq OWNER TO raony;

--
-- Name: diseases_hgmdmutation_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: raony
--

ALTER SEQUENCE diseases_hgmdmutation_id_seq OWNED BY diseases_hgmdmutation.id;


--
-- Name: diseases_hgmdphenotype; Type: TABLE; Schema: public; Owner: raony
--

CREATE TABLE diseases_hgmdphenotype (
    id integer NOT NULL,
    name character varying(255) NOT NULL
);


ALTER TABLE diseases_hgmdphenotype OWNER TO raony;

--
-- Name: diseases_hgmdphenotype_id_seq; Type: SEQUENCE; Schema: public; Owner: raony
--

CREATE SEQUENCE diseases_hgmdphenotype_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE diseases_hgmdphenotype_id_seq OWNER TO raony;

--
-- Name: diseases_hgmdphenotype_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: raony
--

ALTER SEQUENCE diseases_hgmdphenotype_id_seq OWNED BY diseases_hgmdphenotype.id;


--
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: raony
--

CREATE TABLE django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id integer NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);


ALTER TABLE django_admin_log OWNER TO raony;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: raony
--

CREATE SEQUENCE django_admin_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE django_admin_log_id_seq OWNER TO raony;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: raony
--

ALTER SEQUENCE django_admin_log_id_seq OWNED BY django_admin_log.id;


--
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: raony
--

CREATE TABLE django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


ALTER TABLE django_content_type OWNER TO raony;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: raony
--

CREATE SEQUENCE django_content_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE django_content_type_id_seq OWNER TO raony;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: raony
--

ALTER SEQUENCE django_content_type_id_seq OWNED BY django_content_type.id;


--
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: raony
--

CREATE TABLE django_migrations (
    id integer NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


ALTER TABLE django_migrations OWNER TO raony;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: raony
--

CREATE SEQUENCE django_migrations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE django_migrations_id_seq OWNER TO raony;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: raony
--

ALTER SEQUENCE django_migrations_id_seq OWNED BY django_migrations.id;


--
-- Name: django_session; Type: TABLE; Schema: public; Owner: raony
--

CREATE TABLE django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


ALTER TABLE django_session OWNER TO raony;

--
-- Name: django_site; Type: TABLE; Schema: public; Owner: raony
--

CREATE TABLE django_site (
    id integer NOT NULL,
    domain character varying(100) NOT NULL,
    name character varying(50) NOT NULL
);


ALTER TABLE django_site OWNER TO raony;

--
-- Name: django_site_id_seq; Type: SEQUENCE; Schema: public; Owner: raony
--

CREATE SEQUENCE django_site_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE django_site_id_seq OWNER TO raony;

--
-- Name: django_site_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: raony
--

ALTER SEQUENCE django_site_id_seq OWNED BY django_site.id;


--
-- Name: djcelery_crontabschedule; Type: TABLE; Schema: public; Owner: raony
--

CREATE TABLE djcelery_crontabschedule (
    id integer NOT NULL,
    minute character varying(64) NOT NULL,
    hour character varying(64) NOT NULL,
    day_of_week character varying(64) NOT NULL,
    day_of_month character varying(64) NOT NULL,
    month_of_year character varying(64) NOT NULL
);


ALTER TABLE djcelery_crontabschedule OWNER TO raony;

--
-- Name: djcelery_crontabschedule_id_seq; Type: SEQUENCE; Schema: public; Owner: raony
--

CREATE SEQUENCE djcelery_crontabschedule_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE djcelery_crontabschedule_id_seq OWNER TO raony;

--
-- Name: djcelery_crontabschedule_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: raony
--

ALTER SEQUENCE djcelery_crontabschedule_id_seq OWNED BY djcelery_crontabschedule.id;


--
-- Name: djcelery_intervalschedule; Type: TABLE; Schema: public; Owner: raony
--

CREATE TABLE djcelery_intervalschedule (
    id integer NOT NULL,
    every integer NOT NULL,
    period character varying(24) NOT NULL
);


ALTER TABLE djcelery_intervalschedule OWNER TO raony;

--
-- Name: djcelery_intervalschedule_id_seq; Type: SEQUENCE; Schema: public; Owner: raony
--

CREATE SEQUENCE djcelery_intervalschedule_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE djcelery_intervalschedule_id_seq OWNER TO raony;

--
-- Name: djcelery_intervalschedule_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: raony
--

ALTER SEQUENCE djcelery_intervalschedule_id_seq OWNED BY djcelery_intervalschedule.id;


--
-- Name: djcelery_periodictask; Type: TABLE; Schema: public; Owner: raony
--

CREATE TABLE djcelery_periodictask (
    id integer NOT NULL,
    name character varying(200) NOT NULL,
    task character varying(200) NOT NULL,
    args text NOT NULL,
    kwargs text NOT NULL,
    queue character varying(200),
    exchange character varying(200),
    routing_key character varying(200),
    expires timestamp with time zone,
    enabled boolean NOT NULL,
    last_run_at timestamp with time zone,
    total_run_count integer NOT NULL,
    date_changed timestamp with time zone NOT NULL,
    description text NOT NULL,
    crontab_id integer,
    interval_id integer,
    CONSTRAINT djcelery_periodictask_total_run_count_check CHECK ((total_run_count >= 0))
);


ALTER TABLE djcelery_periodictask OWNER TO raony;

--
-- Name: djcelery_periodictask_id_seq; Type: SEQUENCE; Schema: public; Owner: raony
--

CREATE SEQUENCE djcelery_periodictask_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE djcelery_periodictask_id_seq OWNER TO raony;

--
-- Name: djcelery_periodictask_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: raony
--

ALTER SEQUENCE djcelery_periodictask_id_seq OWNED BY djcelery_periodictask.id;


--
-- Name: djcelery_periodictasks; Type: TABLE; Schema: public; Owner: raony
--

CREATE TABLE djcelery_periodictasks (
    ident smallint NOT NULL,
    last_update timestamp with time zone NOT NULL
);


ALTER TABLE djcelery_periodictasks OWNER TO raony;

--
-- Name: djcelery_taskstate; Type: TABLE; Schema: public; Owner: raony
--

CREATE TABLE djcelery_taskstate (
    id integer NOT NULL,
    state character varying(64) NOT NULL,
    task_id character varying(36) NOT NULL,
    name character varying(200),
    tstamp timestamp with time zone NOT NULL,
    args text,
    kwargs text,
    eta timestamp with time zone,
    expires timestamp with time zone,
    result text,
    traceback text,
    runtime double precision,
    retries integer NOT NULL,
    hidden boolean NOT NULL,
    worker_id integer
);


ALTER TABLE djcelery_taskstate OWNER TO raony;

--
-- Name: djcelery_taskstate_id_seq; Type: SEQUENCE; Schema: public; Owner: raony
--

CREATE SEQUENCE djcelery_taskstate_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE djcelery_taskstate_id_seq OWNER TO raony;

--
-- Name: djcelery_taskstate_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: raony
--

ALTER SEQUENCE djcelery_taskstate_id_seq OWNED BY djcelery_taskstate.id;


--
-- Name: djcelery_workerstate; Type: TABLE; Schema: public; Owner: raony
--

CREATE TABLE djcelery_workerstate (
    id integer NOT NULL,
    hostname character varying(255) NOT NULL,
    last_heartbeat timestamp with time zone
);


ALTER TABLE djcelery_workerstate OWNER TO raony;

--
-- Name: djcelery_workerstate_id_seq; Type: SEQUENCE; Schema: public; Owner: raony
--

CREATE SEQUENCE djcelery_workerstate_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE djcelery_workerstate_id_seq OWNER TO raony;

--
-- Name: djcelery_workerstate_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: raony
--

ALTER SEQUENCE djcelery_workerstate_id_seq OWNED BY djcelery_workerstate.id;


--
-- Name: djkombu_message; Type: TABLE; Schema: public; Owner: raony
--

CREATE TABLE djkombu_message (
    id integer NOT NULL,
    visible boolean NOT NULL,
    sent_at timestamp with time zone,
    payload text NOT NULL,
    queue_id integer NOT NULL
);


ALTER TABLE djkombu_message OWNER TO raony;

--
-- Name: djkombu_message_id_seq; Type: SEQUENCE; Schema: public; Owner: raony
--

CREATE SEQUENCE djkombu_message_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE djkombu_message_id_seq OWNER TO raony;

--
-- Name: djkombu_message_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: raony
--

ALTER SEQUENCE djkombu_message_id_seq OWNED BY djkombu_message.id;


--
-- Name: djkombu_queue; Type: TABLE; Schema: public; Owner: raony
--

CREATE TABLE djkombu_queue (
    id integer NOT NULL,
    name character varying(200) NOT NULL
);


ALTER TABLE djkombu_queue OWNER TO raony;

--
-- Name: djkombu_queue_id_seq; Type: SEQUENCE; Schema: public; Owner: raony
--

CREATE SEQUENCE djkombu_queue_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE djkombu_queue_id_seq OWNER TO raony;

--
-- Name: djkombu_queue_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: raony
--

ALTER SEQUENCE djkombu_queue_id_seq OWNED BY djkombu_queue.id;


--
-- Name: files_file; Type: TABLE; Schema: public; Owner: raony
--

CREATE TABLE files_file (
    id integer NOT NULL,
    name text NOT NULL,
    size bigint,
    last_modified timestamp with time zone,
    file_type text,
    location text,
    local_file character varying(600) NOT NULL,
    status text,
    md5 text,
    creation_date timestamp with time zone,
    modified_date timestamp with time zone
);


ALTER TABLE files_file OWNER TO raony;

--
-- Name: files_file_id_seq; Type: SEQUENCE; Schema: public; Owner: raony
--

CREATE SEQUENCE files_file_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE files_file_id_seq OWNER TO raony;

--
-- Name: files_file_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: raony
--

ALTER SEQUENCE files_file_id_seq OWNED BY files_file.id;


--
-- Name: files_s3credential; Type: TABLE; Schema: public; Owner: raony
--

CREATE TABLE files_s3credential (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    access_key character varying(255) NOT NULL,
    secret_key character varying(255) NOT NULL,
    buckets text,
    exclude_paths text,
    exclude_files text
);


ALTER TABLE files_s3credential OWNER TO raony;

--
-- Name: files_s3credential_id_seq; Type: SEQUENCE; Schema: public; Owner: raony
--

CREATE SEQUENCE files_s3credential_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE files_s3credential_id_seq OWNER TO raony;

--
-- Name: files_s3credential_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: raony
--

ALTER SEQUENCE files_s3credential_id_seq OWNED BY files_s3credential.id;


--
-- Name: genes_cgdcondition; Type: TABLE; Schema: public; Owner: raony
--

CREATE TABLE genes_cgdcondition (
    id integer NOT NULL,
    name text NOT NULL
);


ALTER TABLE genes_cgdcondition OWNER TO raony;

--
-- Name: genes_cgdcondition_id_seq; Type: SEQUENCE; Schema: public; Owner: raony
--

CREATE SEQUENCE genes_cgdcondition_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE genes_cgdcondition_id_seq OWNER TO raony;

--
-- Name: genes_cgdcondition_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: raony
--

ALTER SEQUENCE genes_cgdcondition_id_seq OWNED BY genes_cgdcondition.id;


--
-- Name: genes_cgdentry; Type: TABLE; Schema: public; Owner: raony
--

CREATE TABLE genes_cgdentry (
    id integer NOT NULL,
    "GENE" text NOT NULL,
    "HGNC_ID" text NOT NULL,
    "ENTREZ_GENE_ID" text NOT NULL,
    "INHERITANCE" text NOT NULL,
    "AGE_GROUP" text NOT NULL,
    "ALLELIC_CONDITIONS" text NOT NULL,
    "COMMENTS" text NOT NULL,
    "INTERVENTION_RATIONALE" text NOT NULL,
    "REFERENCES" text NOT NULL
);


ALTER TABLE genes_cgdentry OWNER TO raony;

--
-- Name: genes_cgdentry_CONDITIONS; Type: TABLE; Schema: public; Owner: raony
--

CREATE TABLE "genes_cgdentry_CONDITIONS" (
    id integer NOT NULL,
    cgdentry_id integer NOT NULL,
    cgdcondition_id integer NOT NULL
);


ALTER TABLE "genes_cgdentry_CONDITIONS" OWNER TO raony;

--
-- Name: genes_cgdentry_CONDITIONS_id_seq; Type: SEQUENCE; Schema: public; Owner: raony
--

CREATE SEQUENCE "genes_cgdentry_CONDITIONS_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE "genes_cgdentry_CONDITIONS_id_seq" OWNER TO raony;

--
-- Name: genes_cgdentry_CONDITIONS_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: raony
--

ALTER SEQUENCE "genes_cgdentry_CONDITIONS_id_seq" OWNED BY "genes_cgdentry_CONDITIONS".id;


--
-- Name: genes_cgdentry_INTERVENTION_CATEGORIES; Type: TABLE; Schema: public; Owner: raony
--

CREATE TABLE "genes_cgdentry_INTERVENTION_CATEGORIES" (
    id integer NOT NULL,
    cgdentry_id integer NOT NULL,
    intervention_id integer NOT NULL
);


ALTER TABLE "genes_cgdentry_INTERVENTION_CATEGORIES" OWNER TO raony;

--
-- Name: genes_cgdentry_INTERVENTION_CATEGORIES_id_seq; Type: SEQUENCE; Schema: public; Owner: raony
--

CREATE SEQUENCE "genes_cgdentry_INTERVENTION_CATEGORIES_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE "genes_cgdentry_INTERVENTION_CATEGORIES_id_seq" OWNER TO raony;

--
-- Name: genes_cgdentry_INTERVENTION_CATEGORIES_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: raony
--

ALTER SEQUENCE "genes_cgdentry_INTERVENTION_CATEGORIES_id_seq" OWNED BY "genes_cgdentry_INTERVENTION_CATEGORIES".id;


--
-- Name: genes_cgdentry_MANIFESTATION_CATEGORIES; Type: TABLE; Schema: public; Owner: raony
--

CREATE TABLE "genes_cgdentry_MANIFESTATION_CATEGORIES" (
    id integer NOT NULL,
    cgdentry_id integer NOT NULL,
    manifestation_id integer NOT NULL
);


ALTER TABLE "genes_cgdentry_MANIFESTATION_CATEGORIES" OWNER TO raony;

--
-- Name: genes_cgdentry_MANIFESTATION_CATEGORIES_id_seq; Type: SEQUENCE; Schema: public; Owner: raony
--

CREATE SEQUENCE "genes_cgdentry_MANIFESTATION_CATEGORIES_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE "genes_cgdentry_MANIFESTATION_CATEGORIES_id_seq" OWNER TO raony;

--
-- Name: genes_cgdentry_MANIFESTATION_CATEGORIES_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: raony
--

ALTER SEQUENCE "genes_cgdentry_MANIFESTATION_CATEGORIES_id_seq" OWNED BY "genes_cgdentry_MANIFESTATION_CATEGORIES".id;


--
-- Name: genes_cgdentry_id_seq; Type: SEQUENCE; Schema: public; Owner: raony
--

CREATE SEQUENCE genes_cgdentry_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE genes_cgdentry_id_seq OWNER TO raony;

--
-- Name: genes_cgdentry_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: raony
--

ALTER SEQUENCE genes_cgdentry_id_seq OWNED BY genes_cgdentry.id;


--
-- Name: genes_gene; Type: TABLE; Schema: public; Owner: raony
--

CREATE TABLE genes_gene (
    id integer NOT NULL,
    hgnc_id text NOT NULL,
    symbol text NOT NULL,
    name text NOT NULL,
    locus_group text NOT NULL,
    locus_type text NOT NULL,
    status text NOT NULL,
    location text NOT NULL,
    location_sortable text NOT NULL,
    alias_symbol text NOT NULL,
    alias_name text NOT NULL,
    prev_symbol text NOT NULL,
    prev_name text NOT NULL,
    gene_family text NOT NULL,
    gene_family_id text NOT NULL,
    date_approved_reserved text NOT NULL,
    date_symbol_changed text NOT NULL,
    date_name_changed text NOT NULL,
    date_modified text NOT NULL,
    entrez_id text NOT NULL,
    ensembl_gene_id text NOT NULL,
    vega_id text NOT NULL,
    ucsc_id text NOT NULL,
    ena text NOT NULL,
    refseq_accession text NOT NULL,
    ccds_id text NOT NULL,
    uniprot_ids text NOT NULL,
    pubmed_id text NOT NULL,
    mgd_id text NOT NULL,
    rgd_id text NOT NULL,
    lsdb text NOT NULL,
    cosmic text NOT NULL,
    omim_id text NOT NULL,
    mirbase text NOT NULL,
    homeodb text NOT NULL,
    snornabase text NOT NULL,
    bioparadigms_slc text NOT NULL,
    orphanet text NOT NULL,
    pseudogene_org text NOT NULL,
    horde_id text NOT NULL,
    merops text NOT NULL,
    imgt text NOT NULL,
    iuphar text NOT NULL,
    kznf_gene_catalog text NOT NULL,
    mamit_trnadb text NOT NULL,
    cd text NOT NULL,
    lncrnadb text NOT NULL,
    enzyme_id text NOT NULL,
    intermediate_filament_db text NOT NULL
);


ALTER TABLE genes_gene OWNER TO raony;

--
-- Name: genes_gene_diseases; Type: TABLE; Schema: public; Owner: raony
--

CREATE TABLE genes_gene_diseases (
    id integer NOT NULL,
    gene_id integer NOT NULL,
    disease_id integer NOT NULL
);


ALTER TABLE genes_gene_diseases OWNER TO raony;

--
-- Name: genes_gene_diseases_id_seq; Type: SEQUENCE; Schema: public; Owner: raony
--

CREATE SEQUENCE genes_gene_diseases_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE genes_gene_diseases_id_seq OWNER TO raony;

--
-- Name: genes_gene_diseases_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: raony
--

ALTER SEQUENCE genes_gene_diseases_id_seq OWNED BY genes_gene_diseases.id;


--
-- Name: genes_gene_id_seq; Type: SEQUENCE; Schema: public; Owner: raony
--

CREATE SEQUENCE genes_gene_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE genes_gene_id_seq OWNER TO raony;

--
-- Name: genes_gene_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: raony
--

ALTER SEQUENCE genes_gene_id_seq OWNED BY genes_gene.id;


--
-- Name: genes_genecategory; Type: TABLE; Schema: public; Owner: raony
--

CREATE TABLE genes_genecategory (
    id integer NOT NULL,
    domain character varying(255) NOT NULL,
    name text NOT NULL,
    go character varying(255) NOT NULL,
    definition text NOT NULL
);


ALTER TABLE genes_genecategory OWNER TO raony;

--
-- Name: genes_genecategory_genes; Type: TABLE; Schema: public; Owner: raony
--

CREATE TABLE genes_genecategory_genes (
    id integer NOT NULL,
    genecategory_id integer NOT NULL,
    gene_id integer NOT NULL
);


ALTER TABLE genes_genecategory_genes OWNER TO raony;

--
-- Name: genes_genecategory_genes_id_seq; Type: SEQUENCE; Schema: public; Owner: raony
--

CREATE SEQUENCE genes_genecategory_genes_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE genes_genecategory_genes_id_seq OWNER TO raony;

--
-- Name: genes_genecategory_genes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: raony
--

ALTER SEQUENCE genes_genecategory_genes_id_seq OWNED BY genes_genecategory_genes.id;


--
-- Name: genes_genecategory_id_seq; Type: SEQUENCE; Schema: public; Owner: raony
--

CREATE SEQUENCE genes_genecategory_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE genes_genecategory_id_seq OWNER TO raony;

--
-- Name: genes_genecategory_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: raony
--

ALTER SEQUENCE genes_genecategory_id_seq OWNED BY genes_genecategory.id;


--
-- Name: genes_genegroup; Type: TABLE; Schema: public; Owner: raony
--

CREATE TABLE genes_genegroup (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    genes text NOT NULL
);


ALTER TABLE genes_genegroup OWNER TO raony;

--
-- Name: genes_genegroup_id_seq; Type: SEQUENCE; Schema: public; Owner: raony
--

CREATE SEQUENCE genes_genegroup_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE genes_genegroup_id_seq OWNER TO raony;

--
-- Name: genes_genegroup_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: raony
--

ALTER SEQUENCE genes_genegroup_id_seq OWNED BY genes_genegroup.id;


--
-- Name: genes_genelist; Type: TABLE; Schema: public; Owner: raony
--

CREATE TABLE genes_genelist (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    genes text NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE genes_genelist OWNER TO raony;

--
-- Name: genes_genelist_id_seq; Type: SEQUENCE; Schema: public; Owner: raony
--

CREATE SEQUENCE genes_genelist_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE genes_genelist_id_seq OWNER TO raony;

--
-- Name: genes_genelist_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: raony
--

ALTER SEQUENCE genes_genelist_id_seq OWNED BY genes_genelist.id;


--
-- Name: genes_goterm; Type: TABLE; Schema: public; Owner: raony
--

CREATE TABLE genes_goterm (
    id integer NOT NULL,
    goid character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    namespace character varying(255) NOT NULL,
    level character varying(255) NOT NULL,
    is_obsolete boolean NOT NULL,
    alt_ids character varying(255) NOT NULL
);


ALTER TABLE genes_goterm OWNER TO raony;

--
-- Name: genes_goterm_children; Type: TABLE; Schema: public; Owner: raony
--

CREATE TABLE genes_goterm_children (
    id integer NOT NULL,
    from_goterm_id integer NOT NULL,
    to_goterm_id integer NOT NULL
);


ALTER TABLE genes_goterm_children OWNER TO raony;

--
-- Name: genes_goterm_children_id_seq; Type: SEQUENCE; Schema: public; Owner: raony
--

CREATE SEQUENCE genes_goterm_children_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE genes_goterm_children_id_seq OWNER TO raony;

--
-- Name: genes_goterm_children_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: raony
--

ALTER SEQUENCE genes_goterm_children_id_seq OWNED BY genes_goterm_children.id;


--
-- Name: genes_goterm_id_seq; Type: SEQUENCE; Schema: public; Owner: raony
--

CREATE SEQUENCE genes_goterm_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE genes_goterm_id_seq OWNER TO raony;

--
-- Name: genes_goterm_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: raony
--

ALTER SEQUENCE genes_goterm_id_seq OWNED BY genes_goterm.id;


--
-- Name: genes_goterm_parents; Type: TABLE; Schema: public; Owner: raony
--

CREATE TABLE genes_goterm_parents (
    id integer NOT NULL,
    from_goterm_id integer NOT NULL,
    to_goterm_id integer NOT NULL
);


ALTER TABLE genes_goterm_parents OWNER TO raony;

--
-- Name: genes_goterm_parents_id_seq; Type: SEQUENCE; Schema: public; Owner: raony
--

CREATE SEQUENCE genes_goterm_parents_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE genes_goterm_parents_id_seq OWNER TO raony;

--
-- Name: genes_goterm_parents_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: raony
--

ALTER SEQUENCE genes_goterm_parents_id_seq OWNED BY genes_goterm_parents.id;


--
-- Name: genes_intervention; Type: TABLE; Schema: public; Owner: raony
--

CREATE TABLE genes_intervention (
    id integer NOT NULL,
    name text NOT NULL
);


ALTER TABLE genes_intervention OWNER TO raony;

--
-- Name: genes_intervention_id_seq; Type: SEQUENCE; Schema: public; Owner: raony
--

CREATE SEQUENCE genes_intervention_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE genes_intervention_id_seq OWNER TO raony;

--
-- Name: genes_intervention_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: raony
--

ALTER SEQUENCE genes_intervention_id_seq OWNED BY genes_intervention.id;


--
-- Name: genes_manifestation; Type: TABLE; Schema: public; Owner: raony
--

CREATE TABLE genes_manifestation (
    id integer NOT NULL,
    name text NOT NULL
);


ALTER TABLE genes_manifestation OWNER TO raony;

--
-- Name: genes_manifestation_id_seq; Type: SEQUENCE; Schema: public; Owner: raony
--

CREATE SEQUENCE genes_manifestation_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE genes_manifestation_id_seq OWNER TO raony;

--
-- Name: genes_manifestation_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: raony
--

ALTER SEQUENCE genes_manifestation_id_seq OWNED BY genes_manifestation.id;


--
-- Name: genes_membership; Type: TABLE; Schema: public; Owner: raony
--

CREATE TABLE genes_membership (
    id integer NOT NULL,
    gene_id integer NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE genes_membership OWNER TO raony;

--
-- Name: genes_membership_id_seq; Type: SEQUENCE; Schema: public; Owner: raony
--

CREATE SEQUENCE genes_membership_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE genes_membership_id_seq OWNER TO raony;

--
-- Name: genes_membership_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: raony
--

ALTER SEQUENCE genes_membership_id_seq OWNED BY genes_membership.id;


--
-- Name: individuals_controlgroup; Type: TABLE; Schema: public; Owner: raony
--

CREATE TABLE individuals_controlgroup (
    id integer NOT NULL,
    name character varying(600) NOT NULL,
    vcf_file character varying(600) NOT NULL
);


ALTER TABLE individuals_controlgroup OWNER TO raony;

--
-- Name: individuals_controlgroup_id_seq; Type: SEQUENCE; Schema: public; Owner: raony
--

CREATE SEQUENCE individuals_controlgroup_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE individuals_controlgroup_id_seq OWNER TO raony;

--
-- Name: individuals_controlgroup_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: raony
--

ALTER SEQUENCE individuals_controlgroup_id_seq OWNED BY individuals_controlgroup.id;


--
-- Name: individuals_controlvariant; Type: TABLE; Schema: public; Owner: raony
--

CREATE TABLE individuals_controlvariant (
    id integer NOT NULL,
    index text NOT NULL,
    controlgroup_id integer NOT NULL
);


ALTER TABLE individuals_controlvariant OWNER TO raony;

--
-- Name: individuals_controlvariant_id_seq; Type: SEQUENCE; Schema: public; Owner: raony
--

CREATE SEQUENCE individuals_controlvariant_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE individuals_controlvariant_id_seq OWNER TO raony;

--
-- Name: individuals_controlvariant_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: raony
--

ALTER SEQUENCE individuals_controlvariant_id_seq OWNED BY individuals_controlvariant.id;


--
-- Name: individuals_group; Type: TABLE; Schema: public; Owner: raony
--

CREATE TABLE individuals_group (
    id integer NOT NULL,
    name character varying(128) NOT NULL
);


ALTER TABLE individuals_group OWNER TO raony;

--
-- Name: individuals_group_id_seq; Type: SEQUENCE; Schema: public; Owner: raony
--

CREATE SEQUENCE individuals_group_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE individuals_group_id_seq OWNER TO raony;

--
-- Name: individuals_group_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: raony
--

ALTER SEQUENCE individuals_group_id_seq OWNED BY individuals_group.id;


--
-- Name: individuals_group_members; Type: TABLE; Schema: public; Owner: raony
--

CREATE TABLE individuals_group_members (
    id integer NOT NULL,
    group_id integer NOT NULL,
    individual_id integer NOT NULL
);


ALTER TABLE individuals_group_members OWNER TO raony;

--
-- Name: individuals_group_members_id_seq; Type: SEQUENCE; Schema: public; Owner: raony
--

CREATE SEQUENCE individuals_group_members_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE individuals_group_members_id_seq OWNER TO raony;

--
-- Name: individuals_group_members_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: raony
--

ALTER SEQUENCE individuals_group_members_id_seq OWNED BY individuals_group_members.id;


--
-- Name: individuals_individual; Type: TABLE; Schema: public; Owner: raony
--

CREATE TABLE individuals_individual (
    id integer NOT NULL,
    name character varying(600) NOT NULL,
    is_featured boolean NOT NULL,
    is_public boolean NOT NULL,
    vcf_file character varying(600) NOT NULL,
    vcf_header text,
    status character varying(100) NOT NULL,
    n_variants integer,
    n_lines integer,
    creation_date timestamp with time zone,
    modified_date timestamp with time zone,
    annotation_time character varying(200),
    insertion_time character varying(200),
    user_id integer
);


ALTER TABLE individuals_individual OWNER TO raony;

--
-- Name: individuals_individual_id_seq; Type: SEQUENCE; Schema: public; Owner: raony
--

CREATE SEQUENCE individuals_individual_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE individuals_individual_id_seq OWNER TO raony;

--
-- Name: individuals_individual_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: raony
--

ALTER SEQUENCE individuals_individual_id_seq OWNED BY individuals_individual.id;


--
-- Name: individuals_individual_shared_with_groups; Type: TABLE; Schema: public; Owner: raony
--

CREATE TABLE individuals_individual_shared_with_groups (
    id integer NOT NULL,
    individual_id integer NOT NULL,
    usergroup_id integer NOT NULL
);


ALTER TABLE individuals_individual_shared_with_groups OWNER TO raony;

--
-- Name: individuals_individual_shared_with_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: raony
--

CREATE SEQUENCE individuals_individual_shared_with_groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE individuals_individual_shared_with_groups_id_seq OWNER TO raony;

--
-- Name: individuals_individual_shared_with_groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: raony
--

ALTER SEQUENCE individuals_individual_shared_with_groups_id_seq OWNED BY individuals_individual_shared_with_groups.id;


--
-- Name: individuals_individual_shared_with_users; Type: TABLE; Schema: public; Owner: raony
--

CREATE TABLE individuals_individual_shared_with_users (
    id integer NOT NULL,
    individual_id integer NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE individuals_individual_shared_with_users OWNER TO raony;

--
-- Name: individuals_individual_shared_with_users_id_seq; Type: SEQUENCE; Schema: public; Owner: raony
--

CREATE SEQUENCE individuals_individual_shared_with_users_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE individuals_individual_shared_with_users_id_seq OWNER TO raony;

--
-- Name: individuals_individual_shared_with_users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: raony
--

ALTER SEQUENCE individuals_individual_shared_with_users_id_seq OWNED BY individuals_individual_shared_with_users.id;


--
-- Name: individuals_usergroup; Type: TABLE; Schema: public; Owner: raony
--

CREATE TABLE individuals_usergroup (
    id integer NOT NULL,
    name character varying(600) NOT NULL
);


ALTER TABLE individuals_usergroup OWNER TO raony;

--
-- Name: individuals_usergroup_id_seq; Type: SEQUENCE; Schema: public; Owner: raony
--

CREATE SEQUENCE individuals_usergroup_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE individuals_usergroup_id_seq OWNER TO raony;

--
-- Name: individuals_usergroup_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: raony
--

ALTER SEQUENCE individuals_usergroup_id_seq OWNED BY individuals_usergroup.id;


--
-- Name: individuals_usergroup_members; Type: TABLE; Schema: public; Owner: raony
--

CREATE TABLE individuals_usergroup_members (
    id integer NOT NULL,
    usergroup_id integer NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE individuals_usergroup_members OWNER TO raony;

--
-- Name: individuals_usergroup_members_id_seq; Type: SEQUENCE; Schema: public; Owner: raony
--

CREATE SEQUENCE individuals_usergroup_members_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE individuals_usergroup_members_id_seq OWNER TO raony;

--
-- Name: individuals_usergroup_members_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: raony
--

ALTER SEQUENCE individuals_usergroup_members_id_seq OWNED BY individuals_usergroup_members.id;


--
-- Name: projects_project; Type: TABLE; Schema: public; Owner: raony
--

CREATE TABLE projects_project (
    id integer NOT NULL,
    name character varying(30) NOT NULL,
    description text,
    is_public boolean NOT NULL,
    status character varying(100) NOT NULL,
    creation_date timestamp with time zone,
    modified_date timestamp with time zone,
    user_id integer
);


ALTER TABLE projects_project OWNER TO raony;

--
-- Name: projects_project_files; Type: TABLE; Schema: public; Owner: raony
--

CREATE TABLE projects_project_files (
    id integer NOT NULL,
    project_id integer NOT NULL,
    file_id integer NOT NULL
);


ALTER TABLE projects_project_files OWNER TO raony;

--
-- Name: projects_project_files_id_seq; Type: SEQUENCE; Schema: public; Owner: raony
--

CREATE SEQUENCE projects_project_files_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE projects_project_files_id_seq OWNER TO raony;

--
-- Name: projects_project_files_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: raony
--

ALTER SEQUENCE projects_project_files_id_seq OWNED BY projects_project_files.id;


--
-- Name: projects_project_groups; Type: TABLE; Schema: public; Owner: raony
--

CREATE TABLE projects_project_groups (
    id integer NOT NULL,
    project_id integer NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE projects_project_groups OWNER TO raony;

--
-- Name: projects_project_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: raony
--

CREATE SEQUENCE projects_project_groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE projects_project_groups_id_seq OWNER TO raony;

--
-- Name: projects_project_groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: raony
--

ALTER SEQUENCE projects_project_groups_id_seq OWNED BY projects_project_groups.id;


--
-- Name: projects_project_id_seq; Type: SEQUENCE; Schema: public; Owner: raony
--

CREATE SEQUENCE projects_project_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE projects_project_id_seq OWNER TO raony;

--
-- Name: projects_project_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: raony
--

ALTER SEQUENCE projects_project_id_seq OWNED BY projects_project.id;


--
-- Name: projects_project_individuals; Type: TABLE; Schema: public; Owner: raony
--

CREATE TABLE projects_project_individuals (
    id integer NOT NULL,
    project_id integer NOT NULL,
    individual_id integer NOT NULL
);


ALTER TABLE projects_project_individuals OWNER TO raony;

--
-- Name: projects_project_individuals_id_seq; Type: SEQUENCE; Schema: public; Owner: raony
--

CREATE SEQUENCE projects_project_individuals_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE projects_project_individuals_id_seq OWNER TO raony;

--
-- Name: projects_project_individuals_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: raony
--

ALTER SEQUENCE projects_project_individuals_id_seq OWNED BY projects_project_individuals.id;


--
-- Name: projects_project_members; Type: TABLE; Schema: public; Owner: raony
--

CREATE TABLE projects_project_members (
    id integer NOT NULL,
    project_id integer NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE projects_project_members OWNER TO raony;

--
-- Name: projects_project_members_id_seq; Type: SEQUENCE; Schema: public; Owner: raony
--

CREATE SEQUENCE projects_project_members_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE projects_project_members_id_seq OWNER TO raony;

--
-- Name: projects_project_members_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: raony
--

ALTER SEQUENCE projects_project_members_id_seq OWNED BY projects_project_members.id;


--
-- Name: socialaccount_socialaccount; Type: TABLE; Schema: public; Owner: raony
--

CREATE TABLE socialaccount_socialaccount (
    id integer NOT NULL,
    provider character varying(30) NOT NULL,
    uid character varying(191) NOT NULL,
    last_login timestamp with time zone NOT NULL,
    date_joined timestamp with time zone NOT NULL,
    extra_data text NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE socialaccount_socialaccount OWNER TO raony;

--
-- Name: socialaccount_socialaccount_id_seq; Type: SEQUENCE; Schema: public; Owner: raony
--

CREATE SEQUENCE socialaccount_socialaccount_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE socialaccount_socialaccount_id_seq OWNER TO raony;

--
-- Name: socialaccount_socialaccount_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: raony
--

ALTER SEQUENCE socialaccount_socialaccount_id_seq OWNED BY socialaccount_socialaccount.id;


--
-- Name: socialaccount_socialapp; Type: TABLE; Schema: public; Owner: raony
--

CREATE TABLE socialaccount_socialapp (
    id integer NOT NULL,
    provider character varying(30) NOT NULL,
    name character varying(40) NOT NULL,
    client_id character varying(191) NOT NULL,
    secret character varying(191) NOT NULL,
    key character varying(191) NOT NULL
);


ALTER TABLE socialaccount_socialapp OWNER TO raony;

--
-- Name: socialaccount_socialapp_id_seq; Type: SEQUENCE; Schema: public; Owner: raony
--

CREATE SEQUENCE socialaccount_socialapp_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE socialaccount_socialapp_id_seq OWNER TO raony;

--
-- Name: socialaccount_socialapp_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: raony
--

ALTER SEQUENCE socialaccount_socialapp_id_seq OWNED BY socialaccount_socialapp.id;


--
-- Name: socialaccount_socialapp_sites; Type: TABLE; Schema: public; Owner: raony
--

CREATE TABLE socialaccount_socialapp_sites (
    id integer NOT NULL,
    socialapp_id integer NOT NULL,
    site_id integer NOT NULL
);


ALTER TABLE socialaccount_socialapp_sites OWNER TO raony;

--
-- Name: socialaccount_socialapp_sites_id_seq; Type: SEQUENCE; Schema: public; Owner: raony
--

CREATE SEQUENCE socialaccount_socialapp_sites_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE socialaccount_socialapp_sites_id_seq OWNER TO raony;

--
-- Name: socialaccount_socialapp_sites_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: raony
--

ALTER SEQUENCE socialaccount_socialapp_sites_id_seq OWNED BY socialaccount_socialapp_sites.id;


--
-- Name: socialaccount_socialtoken; Type: TABLE; Schema: public; Owner: raony
--

CREATE TABLE socialaccount_socialtoken (
    id integer NOT NULL,
    token text NOT NULL,
    token_secret text NOT NULL,
    expires_at timestamp with time zone,
    account_id integer NOT NULL,
    app_id integer NOT NULL
);


ALTER TABLE socialaccount_socialtoken OWNER TO raony;

--
-- Name: socialaccount_socialtoken_id_seq; Type: SEQUENCE; Schema: public; Owner: raony
--

CREATE SEQUENCE socialaccount_socialtoken_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE socialaccount_socialtoken_id_seq OWNER TO raony;

--
-- Name: socialaccount_socialtoken_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: raony
--

ALTER SEQUENCE socialaccount_socialtoken_id_seq OWNED BY socialaccount_socialtoken.id;


--
-- Name: variants_variant; Type: TABLE; Schema: public; Owner: raony
--

CREATE TABLE variants_variant (
    id integer NOT NULL,
    chr character varying(2) NOT NULL,
    pos integer NOT NULL,
    index text
);


ALTER TABLE variants_variant OWNER TO raony;

--
-- Name: variants_variant_id_seq; Type: SEQUENCE; Schema: public; Owner: raony
--

CREATE SEQUENCE variants_variant_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE variants_variant_id_seq OWNER TO raony;

--
-- Name: variants_variant_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: raony
--

ALTER SEQUENCE variants_variant_id_seq OWNED BY variants_variant.id;


--
-- Name: variants_variantannotation; Type: TABLE; Schema: public; Owner: raony
--

CREATE TABLE variants_variantannotation (
    id integer NOT NULL,
    variant_id text NOT NULL,
    ref text,
    alt text,
    qual double precision NOT NULL,
    filter text NOT NULL,
    info text,
    format text,
    genotype_col text,
    genotype text NOT NULL,
    read_depth integer NOT NULL,
    gene text,
    mutation_type text,
    vartype text,
    genomes1k_maf double precision,
    dbsnp_maf double precision,
    esp_maf double precision,
    dbsnp_build integer,
    sift double precision,
    sift_pred text,
    polyphen2 double precision,
    polyphen2_pred text,
    condel double precision,
    condel_pred text,
    dann double precision,
    cadd double precision,
    hi_index_str text,
    hi_index double precision,
    hi_index_perc double precision,
    is_at_omim boolean NOT NULL,
    is_at_hgmd boolean NOT NULL,
    hgmd_entries text,
    snpeff_effect text,
    snpeff_impact text,
    snpeff_func_class text,
    snpeff_codon_change text,
    snpeff_aa_change text,
    snpeff_gene_name text,
    snpeff_biotype text,
    snpeff_gene_coding text,
    snpeff_transcript_id text,
    snpeff_exon_rank text,
    vep_allele text,
    vep_gene text,
    vep_feature text,
    vep_feature_type text,
    vep_consequence text,
    vep_cdna_position text,
    vep_cds_position text,
    vep_protein_position text,
    vep_amino_acids text,
    vep_codons text,
    vep_existing_variation text,
    vep_distance text,
    vep_strand text,
    vep_symbol text,
    vep_symbol_source text,
    vep_sift text,
    vep_polyphen text,
    vep_condel text,
    "ensembl_clin_HGMD" boolean NOT NULL,
    "clinvar_CLNSRC" text,
    "SIFT_score" text,
    "SIFT_converted_rankscore" text,
    "Uniprot_acc_Polyphen2" text,
    "Uniprot_id_Polyphen2" text,
    "Uniprot_aapos_Polyphen2" text,
    "Polyphen2_HDIV_score" text,
    "Polyphen2_HDIV_rankscore" text,
    "Polyphen2_HDIV_pred" text,
    "Polyphen2_HVAR_score" text,
    "Polyphen2_HVAR_rankscore" text,
    "Polyphen2_HVAR_pred" text,
    "LRT_score" text,
    "LRT_converted_rankscore" text,
    "LRT_pred" text,
    "LRT_Omega" text,
    "MutationTaster_score" text,
    "MutationTaster_converted_rankscore" text,
    "MutationTaster_pred" text,
    "MutationTaster_model" text,
    "MutationTaster_AAE" text,
    "MutationAssessor_UniprotID" text,
    "MutationAssessor_variant" text,
    "MutationAssessor_score" text,
    "MutationAssessor_rankscore" text,
    "MutationAssessor_pred" text,
    "FATHMM_score" text,
    "FATHMM_converted_rankscore" text,
    "FATHMM_pred" text,
    "PROVEAN_score" text,
    "PROVEAN_converted_rankscore" text,
    "PROVEAN_pred" text,
    "Transcript_id_VEST3" text,
    "Transcript_var_VEST3" text,
    "VEST3_score" text,
    "VEST3_rankscore" text,
    "MetaSVM_score" text,
    "MetaSVM_rankscore" text,
    "MetaSVM_pred" text,
    "MetaLR_score" text,
    "MetaLR_rankscore" text,
    "MetaLR_pred" text,
    "Reliability_index" text,
    "CADD_raw" text,
    "CADD_raw_rankscore" text,
    "CADD_phred" text,
    "DANN_score" text,
    "DANN_rankscore" text,
    "fathmm_MKL_coding_score" text,
    "fathmm_MKL_coding_rankscore" text,
    "fathmm_MKL_coding_pred" text,
    "fathmm_MKL_coding_group" text,
    "Eigen_raw" text,
    "Eigen_phred" text,
    "Eigen_raw_rankscore" text,
    "Eigen_PC_raw" text,
    "Eigen_PC_raw_rankscore" text,
    "GenoCanyon_score" text,
    "GenoCanyon_score_rankscore" text,
    "integrated_fitCons_score" text,
    "integrated_fitCons_rankscore" text,
    integrated_confidence_value text,
    "GM12878_fitCons_score" text,
    "GM12878_fitCons_rankscore" text,
    "GM12878_confidence_value" text,
    "H1_hESC_fitCons_score" text,
    "H1_hESC_fitCons_rankscore" text,
    "H1_hESC_confidence_value" text,
    "HUVEC_fitCons_score" text,
    "HUVEC_fitCons_rankscore" text,
    "HUVEC_confidence_value" text,
    "GERP_NR" text,
    "GERP_RS" text,
    "GERP_RS_rankscore" text,
    "phyloP100way_vertebrate" text,
    "phyloP100way_vertebrate_rankscore" text,
    "phyloP20way_mammalian" text,
    "phyloP20way_mammalian_rankscore" text,
    "phastCons100way_vertebrate" text,
    "phastCons100way_vertebrate_rankscore" text,
    "phastCons20way_mammalian" text,
    "phastCons20way_mammalian_rankscore" text,
    "SiPhy_29way_pi" text,
    "SiPhy_29way_logOdds" text,
    "SiPhy_29way_logOdds_rankscore" text,
    clinvar_rs text,
    clinvar_clnsig text,
    clinvar_trait text,
    clinvar_golden_stars text,
    mcap_score double precision,
    mcap_rankscore double precision,
    mcap_pred text,
    revel_score text
);


ALTER TABLE variants_variantannotation OWNER TO raony;

--
-- Name: variants_variantannotation_id_seq; Type: SEQUENCE; Schema: public; Owner: raony
--

CREATE SEQUENCE variants_variantannotation_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE variants_variantannotation_id_seq OWNER TO raony;

--
-- Name: variants_variantannotation_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: raony
--

ALTER SEQUENCE variants_variantannotation_id_seq OWNED BY variants_variantannotation.id;


--
-- Name: account_emailaddress id; Type: DEFAULT; Schema: public; Owner: raony
--

ALTER TABLE ONLY account_emailaddress ALTER COLUMN id SET DEFAULT nextval('account_emailaddress_id_seq'::regclass);


--
-- Name: account_emailconfirmation id; Type: DEFAULT; Schema: public; Owner: raony
--

ALTER TABLE ONLY account_emailconfirmation ALTER COLUMN id SET DEFAULT nextval('account_emailconfirmation_id_seq'::regclass);


--
-- Name: auth_group id; Type: DEFAULT; Schema: public; Owner: raony
--

ALTER TABLE ONLY auth_group ALTER COLUMN id SET DEFAULT nextval('auth_group_id_seq'::regclass);


--
-- Name: auth_group_permissions id; Type: DEFAULT; Schema: public; Owner: raony
--

ALTER TABLE ONLY auth_group_permissions ALTER COLUMN id SET DEFAULT nextval('auth_group_permissions_id_seq'::regclass);


--
-- Name: auth_permission id; Type: DEFAULT; Schema: public; Owner: raony
--

ALTER TABLE ONLY auth_permission ALTER COLUMN id SET DEFAULT nextval('auth_permission_id_seq'::regclass);


--
-- Name: auth_user id; Type: DEFAULT; Schema: public; Owner: raony
--

ALTER TABLE ONLY auth_user ALTER COLUMN id SET DEFAULT nextval('auth_user_id_seq'::regclass);


--
-- Name: auth_user_groups id; Type: DEFAULT; Schema: public; Owner: raony
--

ALTER TABLE ONLY auth_user_groups ALTER COLUMN id SET DEFAULT nextval('auth_user_groups_id_seq'::regclass);


--
-- Name: auth_user_user_permissions id; Type: DEFAULT; Schema: public; Owner: raony
--

ALTER TABLE ONLY auth_user_user_permissions ALTER COLUMN id SET DEFAULT nextval('auth_user_user_permissions_id_seq'::regclass);


--
-- Name: cases_case id; Type: DEFAULT; Schema: public; Owner: raony
--

ALTER TABLE ONLY cases_case ALTER COLUMN id SET DEFAULT nextval('cases_case_id_seq'::regclass);


--
-- Name: cases_case_case_groups id; Type: DEFAULT; Schema: public; Owner: raony
--

ALTER TABLE ONLY cases_case_case_groups ALTER COLUMN id SET DEFAULT nextval('cases_case_case_groups_id_seq'::regclass);


--
-- Name: cases_case_cases id; Type: DEFAULT; Schema: public; Owner: raony
--

ALTER TABLE ONLY cases_case_cases ALTER COLUMN id SET DEFAULT nextval('cases_case_cases_id_seq'::regclass);


--
-- Name: cases_case_children id; Type: DEFAULT; Schema: public; Owner: raony
--

ALTER TABLE ONLY cases_case_children ALTER COLUMN id SET DEFAULT nextval('cases_case_children_id_seq'::regclass);


--
-- Name: cases_case_control_groups id; Type: DEFAULT; Schema: public; Owner: raony
--

ALTER TABLE ONLY cases_case_control_groups ALTER COLUMN id SET DEFAULT nextval('cases_case_control_groups_id_seq'::regclass);


--
-- Name: cases_case_controls id; Type: DEFAULT; Schema: public; Owner: raony
--

ALTER TABLE ONLY cases_case_controls ALTER COLUMN id SET DEFAULT nextval('cases_case_controls_id_seq'::regclass);


--
-- Name: cases_case_shared_with_groups id; Type: DEFAULT; Schema: public; Owner: raony
--

ALTER TABLE ONLY cases_case_shared_with_groups ALTER COLUMN id SET DEFAULT nextval('cases_case_shared_with_groups_id_seq'::regclass);


--
-- Name: cases_case_shared_with_users id; Type: DEFAULT; Schema: public; Owner: raony
--

ALTER TABLE ONLY cases_case_shared_with_users ALTER COLUMN id SET DEFAULT nextval('cases_case_shared_with_users_id_seq'::regclass);


--
-- Name: celery_taskmeta id; Type: DEFAULT; Schema: public; Owner: raony
--

ALTER TABLE ONLY celery_taskmeta ALTER COLUMN id SET DEFAULT nextval('celery_taskmeta_id_seq'::regclass);


--
-- Name: celery_tasksetmeta id; Type: DEFAULT; Schema: public; Owner: raony
--

ALTER TABLE ONLY celery_tasksetmeta ALTER COLUMN id SET DEFAULT nextval('celery_tasksetmeta_id_seq'::regclass);


--
-- Name: diseases_disease id; Type: DEFAULT; Schema: public; Owner: raony
--

ALTER TABLE ONLY diseases_disease ALTER COLUMN id SET DEFAULT nextval('diseases_disease_id_seq'::regclass);


--
-- Name: diseases_gene id; Type: DEFAULT; Schema: public; Owner: raony
--

ALTER TABLE ONLY diseases_gene ALTER COLUMN id SET DEFAULT nextval('diseases_gene_id_seq'::regclass);


--
-- Name: diseases_gene_diseases id; Type: DEFAULT; Schema: public; Owner: raony
--

ALTER TABLE ONLY diseases_gene_diseases ALTER COLUMN id SET DEFAULT nextval('diseases_gene_diseases_id_seq'::regclass);


--
-- Name: diseases_hgmdgene id; Type: DEFAULT; Schema: public; Owner: raony
--

ALTER TABLE ONLY diseases_hgmdgene ALTER COLUMN id SET DEFAULT nextval('diseases_hgmdgene_id_seq'::regclass);


--
-- Name: diseases_hgmdgene_diseases id; Type: DEFAULT; Schema: public; Owner: raony
--

ALTER TABLE ONLY diseases_hgmdgene_diseases ALTER COLUMN id SET DEFAULT nextval('diseases_hgmdgene_diseases_id_seq'::regclass);


--
-- Name: diseases_hgmdmutation id; Type: DEFAULT; Schema: public; Owner: raony
--

ALTER TABLE ONLY diseases_hgmdmutation ALTER COLUMN id SET DEFAULT nextval('diseases_hgmdmutation_id_seq'::regclass);


--
-- Name: diseases_hgmdphenotype id; Type: DEFAULT; Schema: public; Owner: raony
--

ALTER TABLE ONLY diseases_hgmdphenotype ALTER COLUMN id SET DEFAULT nextval('diseases_hgmdphenotype_id_seq'::regclass);


--
-- Name: django_admin_log id; Type: DEFAULT; Schema: public; Owner: raony
--

ALTER TABLE ONLY django_admin_log ALTER COLUMN id SET DEFAULT nextval('django_admin_log_id_seq'::regclass);


--
-- Name: django_content_type id; Type: DEFAULT; Schema: public; Owner: raony
--

ALTER TABLE ONLY django_content_type ALTER COLUMN id SET DEFAULT nextval('django_content_type_id_seq'::regclass);


--
-- Name: django_migrations id; Type: DEFAULT; Schema: public; Owner: raony
--

ALTER TABLE ONLY django_migrations ALTER COLUMN id SET DEFAULT nextval('django_migrations_id_seq'::regclass);


--
-- Name: django_site id; Type: DEFAULT; Schema: public; Owner: raony
--

ALTER TABLE ONLY django_site ALTER COLUMN id SET DEFAULT nextval('django_site_id_seq'::regclass);


--
-- Name: djcelery_crontabschedule id; Type: DEFAULT; Schema: public; Owner: raony
--

ALTER TABLE ONLY djcelery_crontabschedule ALTER COLUMN id SET DEFAULT nextval('djcelery_crontabschedule_id_seq'::regclass);


--
-- Name: djcelery_intervalschedule id; Type: DEFAULT; Schema: public; Owner: raony
--

ALTER TABLE ONLY djcelery_intervalschedule ALTER COLUMN id SET DEFAULT nextval('djcelery_intervalschedule_id_seq'::regclass);


--
-- Name: djcelery_periodictask id; Type: DEFAULT; Schema: public; Owner: raony
--

ALTER TABLE ONLY djcelery_periodictask ALTER COLUMN id SET DEFAULT nextval('djcelery_periodictask_id_seq'::regclass);


--
-- Name: djcelery_taskstate id; Type: DEFAULT; Schema: public; Owner: raony
--

ALTER TABLE ONLY djcelery_taskstate ALTER COLUMN id SET DEFAULT nextval('djcelery_taskstate_id_seq'::regclass);


--
-- Name: djcelery_workerstate id; Type: DEFAULT; Schema: public; Owner: raony
--

ALTER TABLE ONLY djcelery_workerstate ALTER COLUMN id SET DEFAULT nextval('djcelery_workerstate_id_seq'::regclass);


--
-- Name: djkombu_message id; Type: DEFAULT; Schema: public; Owner: raony
--

ALTER TABLE ONLY djkombu_message ALTER COLUMN id SET DEFAULT nextval('djkombu_message_id_seq'::regclass);


--
-- Name: djkombu_queue id; Type: DEFAULT; Schema: public; Owner: raony
--

ALTER TABLE ONLY djkombu_queue ALTER COLUMN id SET DEFAULT nextval('djkombu_queue_id_seq'::regclass);


--
-- Name: files_file id; Type: DEFAULT; Schema: public; Owner: raony
--

ALTER TABLE ONLY files_file ALTER COLUMN id SET DEFAULT nextval('files_file_id_seq'::regclass);


--
-- Name: files_s3credential id; Type: DEFAULT; Schema: public; Owner: raony
--

ALTER TABLE ONLY files_s3credential ALTER COLUMN id SET DEFAULT nextval('files_s3credential_id_seq'::regclass);


--
-- Name: genes_cgdcondition id; Type: DEFAULT; Schema: public; Owner: raony
--

ALTER TABLE ONLY genes_cgdcondition ALTER COLUMN id SET DEFAULT nextval('genes_cgdcondition_id_seq'::regclass);


--
-- Name: genes_cgdentry id; Type: DEFAULT; Schema: public; Owner: raony
--

ALTER TABLE ONLY genes_cgdentry ALTER COLUMN id SET DEFAULT nextval('genes_cgdentry_id_seq'::regclass);


--
-- Name: genes_cgdentry_CONDITIONS id; Type: DEFAULT; Schema: public; Owner: raony
--

ALTER TABLE ONLY "genes_cgdentry_CONDITIONS" ALTER COLUMN id SET DEFAULT nextval('"genes_cgdentry_CONDITIONS_id_seq"'::regclass);


--
-- Name: genes_cgdentry_INTERVENTION_CATEGORIES id; Type: DEFAULT; Schema: public; Owner: raony
--

ALTER TABLE ONLY "genes_cgdentry_INTERVENTION_CATEGORIES" ALTER COLUMN id SET DEFAULT nextval('"genes_cgdentry_INTERVENTION_CATEGORIES_id_seq"'::regclass);


--
-- Name: genes_cgdentry_MANIFESTATION_CATEGORIES id; Type: DEFAULT; Schema: public; Owner: raony
--

ALTER TABLE ONLY "genes_cgdentry_MANIFESTATION_CATEGORIES" ALTER COLUMN id SET DEFAULT nextval('"genes_cgdentry_MANIFESTATION_CATEGORIES_id_seq"'::regclass);


--
-- Name: genes_gene id; Type: DEFAULT; Schema: public; Owner: raony
--

ALTER TABLE ONLY genes_gene ALTER COLUMN id SET DEFAULT nextval('genes_gene_id_seq'::regclass);


--
-- Name: genes_gene_diseases id; Type: DEFAULT; Schema: public; Owner: raony
--

ALTER TABLE ONLY genes_gene_diseases ALTER COLUMN id SET DEFAULT nextval('genes_gene_diseases_id_seq'::regclass);


--
-- Name: genes_genecategory id; Type: DEFAULT; Schema: public; Owner: raony
--

ALTER TABLE ONLY genes_genecategory ALTER COLUMN id SET DEFAULT nextval('genes_genecategory_id_seq'::regclass);


--
-- Name: genes_genecategory_genes id; Type: DEFAULT; Schema: public; Owner: raony
--

ALTER TABLE ONLY genes_genecategory_genes ALTER COLUMN id SET DEFAULT nextval('genes_genecategory_genes_id_seq'::regclass);


--
-- Name: genes_genegroup id; Type: DEFAULT; Schema: public; Owner: raony
--

ALTER TABLE ONLY genes_genegroup ALTER COLUMN id SET DEFAULT nextval('genes_genegroup_id_seq'::regclass);


--
-- Name: genes_genelist id; Type: DEFAULT; Schema: public; Owner: raony
--

ALTER TABLE ONLY genes_genelist ALTER COLUMN id SET DEFAULT nextval('genes_genelist_id_seq'::regclass);


--
-- Name: genes_goterm id; Type: DEFAULT; Schema: public; Owner: raony
--

ALTER TABLE ONLY genes_goterm ALTER COLUMN id SET DEFAULT nextval('genes_goterm_id_seq'::regclass);


--
-- Name: genes_goterm_children id; Type: DEFAULT; Schema: public; Owner: raony
--

ALTER TABLE ONLY genes_goterm_children ALTER COLUMN id SET DEFAULT nextval('genes_goterm_children_id_seq'::regclass);


--
-- Name: genes_goterm_parents id; Type: DEFAULT; Schema: public; Owner: raony
--

ALTER TABLE ONLY genes_goterm_parents ALTER COLUMN id SET DEFAULT nextval('genes_goterm_parents_id_seq'::regclass);


--
-- Name: genes_intervention id; Type: DEFAULT; Schema: public; Owner: raony
--

ALTER TABLE ONLY genes_intervention ALTER COLUMN id SET DEFAULT nextval('genes_intervention_id_seq'::regclass);


--
-- Name: genes_manifestation id; Type: DEFAULT; Schema: public; Owner: raony
--

ALTER TABLE ONLY genes_manifestation ALTER COLUMN id SET DEFAULT nextval('genes_manifestation_id_seq'::regclass);


--
-- Name: genes_membership id; Type: DEFAULT; Schema: public; Owner: raony
--

ALTER TABLE ONLY genes_membership ALTER COLUMN id SET DEFAULT nextval('genes_membership_id_seq'::regclass);


--
-- Name: individuals_controlgroup id; Type: DEFAULT; Schema: public; Owner: raony
--

ALTER TABLE ONLY individuals_controlgroup ALTER COLUMN id SET DEFAULT nextval('individuals_controlgroup_id_seq'::regclass);


--
-- Name: individuals_controlvariant id; Type: DEFAULT; Schema: public; Owner: raony
--

ALTER TABLE ONLY individuals_controlvariant ALTER COLUMN id SET DEFAULT nextval('individuals_controlvariant_id_seq'::regclass);


--
-- Name: individuals_group id; Type: DEFAULT; Schema: public; Owner: raony
--

ALTER TABLE ONLY individuals_group ALTER COLUMN id SET DEFAULT nextval('individuals_group_id_seq'::regclass);


--
-- Name: individuals_group_members id; Type: DEFAULT; Schema: public; Owner: raony
--

ALTER TABLE ONLY individuals_group_members ALTER COLUMN id SET DEFAULT nextval('individuals_group_members_id_seq'::regclass);


--
-- Name: individuals_individual id; Type: DEFAULT; Schema: public; Owner: raony
--

ALTER TABLE ONLY individuals_individual ALTER COLUMN id SET DEFAULT nextval('individuals_individual_id_seq'::regclass);


--
-- Name: individuals_individual_shared_with_groups id; Type: DEFAULT; Schema: public; Owner: raony
--

ALTER TABLE ONLY individuals_individual_shared_with_groups ALTER COLUMN id SET DEFAULT nextval('individuals_individual_shared_with_groups_id_seq'::regclass);


--
-- Name: individuals_individual_shared_with_users id; Type: DEFAULT; Schema: public; Owner: raony
--

ALTER TABLE ONLY individuals_individual_shared_with_users ALTER COLUMN id SET DEFAULT nextval('individuals_individual_shared_with_users_id_seq'::regclass);


--
-- Name: individuals_usergroup id; Type: DEFAULT; Schema: public; Owner: raony
--

ALTER TABLE ONLY individuals_usergroup ALTER COLUMN id SET DEFAULT nextval('individuals_usergroup_id_seq'::regclass);


--
-- Name: individuals_usergroup_members id; Type: DEFAULT; Schema: public; Owner: raony
--

ALTER TABLE ONLY individuals_usergroup_members ALTER COLUMN id SET DEFAULT nextval('individuals_usergroup_members_id_seq'::regclass);


--
-- Name: projects_project id; Type: DEFAULT; Schema: public; Owner: raony
--

ALTER TABLE ONLY projects_project ALTER COLUMN id SET DEFAULT nextval('projects_project_id_seq'::regclass);


--
-- Name: projects_project_files id; Type: DEFAULT; Schema: public; Owner: raony
--

ALTER TABLE ONLY projects_project_files ALTER COLUMN id SET DEFAULT nextval('projects_project_files_id_seq'::regclass);


--
-- Name: projects_project_groups id; Type: DEFAULT; Schema: public; Owner: raony
--

ALTER TABLE ONLY projects_project_groups ALTER COLUMN id SET DEFAULT nextval('projects_project_groups_id_seq'::regclass);


--
-- Name: projects_project_individuals id; Type: DEFAULT; Schema: public; Owner: raony
--

ALTER TABLE ONLY projects_project_individuals ALTER COLUMN id SET DEFAULT nextval('projects_project_individuals_id_seq'::regclass);


--
-- Name: projects_project_members id; Type: DEFAULT; Schema: public; Owner: raony
--

ALTER TABLE ONLY projects_project_members ALTER COLUMN id SET DEFAULT nextval('projects_project_members_id_seq'::regclass);


--
-- Name: socialaccount_socialaccount id; Type: DEFAULT; Schema: public; Owner: raony
--

ALTER TABLE ONLY socialaccount_socialaccount ALTER COLUMN id SET DEFAULT nextval('socialaccount_socialaccount_id_seq'::regclass);


--
-- Name: socialaccount_socialapp id; Type: DEFAULT; Schema: public; Owner: raony
--

ALTER TABLE ONLY socialaccount_socialapp ALTER COLUMN id SET DEFAULT nextval('socialaccount_socialapp_id_seq'::regclass);


--
-- Name: socialaccount_socialapp_sites id; Type: DEFAULT; Schema: public; Owner: raony
--

ALTER TABLE ONLY socialaccount_socialapp_sites ALTER COLUMN id SET DEFAULT nextval('socialaccount_socialapp_sites_id_seq'::regclass);


--
-- Name: socialaccount_socialtoken id; Type: DEFAULT; Schema: public; Owner: raony
--

ALTER TABLE ONLY socialaccount_socialtoken ALTER COLUMN id SET DEFAULT nextval('socialaccount_socialtoken_id_seq'::regclass);


--
-- Name: variants_variant id; Type: DEFAULT; Schema: public; Owner: raony
--

ALTER TABLE ONLY variants_variant ALTER COLUMN id SET DEFAULT nextval('variants_variant_id_seq'::regclass);


--
-- Name: variants_variantannotation id; Type: DEFAULT; Schema: public; Owner: raony
--

ALTER TABLE ONLY variants_variantannotation ALTER COLUMN id SET DEFAULT nextval('variants_variantannotation_id_seq'::regclass);


--
-- Data for Name: account_emailaddress; Type: TABLE DATA; Schema: public; Owner: raony
--

COPY account_emailaddress (id, email, verified, "primary", user_id) FROM stdin;
\.


--
-- Name: account_emailaddress_id_seq; Type: SEQUENCE SET; Schema: public; Owner: raony
--

SELECT pg_catalog.setval('account_emailaddress_id_seq', 1, false);


--
-- Data for Name: account_emailconfirmation; Type: TABLE DATA; Schema: public; Owner: raony
--

COPY account_emailconfirmation (id, created, sent, key, email_address_id) FROM stdin;
\.


--
-- Name: account_emailconfirmation_id_seq; Type: SEQUENCE SET; Schema: public; Owner: raony
--

SELECT pg_catalog.setval('account_emailconfirmation_id_seq', 1, false);


--
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: raony
--

COPY auth_group (id, name) FROM stdin;
\.


--
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: raony
--

SELECT pg_catalog.setval('auth_group_id_seq', 1, false);


--
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: raony
--

COPY auth_group_permissions (id, group_id, permission_id) FROM stdin;
\.


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: raony
--

SELECT pg_catalog.setval('auth_group_permissions_id_seq', 1, false);


--
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: raony
--

COPY auth_permission (id, name, content_type_id, codename) FROM stdin;
1	Can add log entry	1	add_logentry
2	Can change log entry	1	change_logentry
3	Can delete log entry	1	delete_logentry
4	Can add permission	2	add_permission
5	Can change permission	2	change_permission
6	Can delete permission	2	delete_permission
7	Can add group	3	add_group
8	Can change group	3	change_group
9	Can delete group	3	delete_group
10	Can add user	4	add_user
11	Can change user	4	change_user
12	Can delete user	4	delete_user
13	Can add content type	5	add_contenttype
14	Can change content type	5	change_contenttype
15	Can delete content type	5	delete_contenttype
16	Can add session	6	add_session
17	Can change session	6	change_session
18	Can delete session	6	delete_session
19	Can add site	7	add_site
20	Can change site	7	change_site
21	Can delete site	7	delete_site
22	Can add email address	8	add_emailaddress
23	Can change email address	8	change_emailaddress
24	Can delete email address	8	delete_emailaddress
25	Can add email confirmation	9	add_emailconfirmation
26	Can change email confirmation	9	change_emailconfirmation
27	Can delete email confirmation	9	delete_emailconfirmation
28	Can add social account	10	add_socialaccount
29	Can change social account	10	change_socialaccount
30	Can delete social account	10	delete_socialaccount
31	Can add social application	11	add_socialapp
32	Can change social application	11	change_socialapp
33	Can delete social application	11	delete_socialapp
34	Can add social application token	12	add_socialtoken
35	Can change social application token	12	change_socialtoken
36	Can delete social application token	12	delete_socialtoken
37	Can add crontab	13	add_crontabschedule
38	Can change crontab	13	change_crontabschedule
39	Can delete crontab	13	delete_crontabschedule
40	Can add interval	14	add_intervalschedule
41	Can change interval	14	change_intervalschedule
42	Can delete interval	14	delete_intervalschedule
43	Can add periodic task	15	add_periodictask
44	Can change periodic task	15	change_periodictask
45	Can delete periodic task	15	delete_periodictask
46	Can add periodic tasks	16	add_periodictasks
47	Can change periodic tasks	16	change_periodictasks
48	Can delete periodic tasks	16	delete_periodictasks
49	Can add task state	17	add_taskmeta
50	Can change task state	17	change_taskmeta
51	Can delete task state	17	delete_taskmeta
52	Can add saved group result	18	add_tasksetmeta
53	Can change saved group result	18	change_tasksetmeta
54	Can delete saved group result	18	delete_tasksetmeta
55	Can add task	19	add_taskstate
56	Can change task	19	change_taskstate
57	Can delete task	19	delete_taskstate
58	Can add worker	20	add_workerstate
59	Can change worker	20	change_workerstate
60	Can delete worker	20	delete_workerstate
61	Can add message	21	add_message
62	Can change message	21	change_message
63	Can delete message	21	delete_message
64	Can add queue	22	add_queue
65	Can change queue	22	change_queue
66	Can delete queue	22	delete_queue
67	Can add control group	23	add_controlgroup
68	Can change control group	23	change_controlgroup
69	Can delete control group	23	delete_controlgroup
70	Can add control variant	24	add_controlvariant
71	Can change control variant	24	change_controlvariant
72	Can delete control variant	24	delete_controlvariant
73	Can add group	25	add_group
74	Can change group	25	change_group
75	Can delete group	25	delete_group
76	Can add individual	26	add_individual
77	Can change individual	26	change_individual
78	Can delete individual	26	delete_individual
79	Can add user group	27	add_usergroup
80	Can change user group	27	change_usergroup
81	Can delete user group	27	delete_usergroup
82	Can add variant	28	add_variant
83	Can change variant	28	change_variant
84	Can delete variant	28	delete_variant
85	Can add variant annotation	29	add_variantannotation
86	Can change variant annotation	29	change_variantannotation
87	Can delete variant annotation	29	delete_variantannotation
88	Can add disease	30	add_disease
89	Can change disease	30	change_disease
90	Can delete disease	30	delete_disease
91	Can add gene	31	add_gene
92	Can change gene	31	change_gene
93	Can delete gene	31	delete_gene
94	Can add hgmd gene	32	add_hgmdgene
95	Can change hgmd gene	32	change_hgmdgene
96	Can delete hgmd gene	32	delete_hgmdgene
97	Can add hgmd mutation	33	add_hgmdmutation
98	Can change hgmd mutation	33	change_hgmdmutation
99	Can delete hgmd mutation	33	delete_hgmdmutation
100	Can add hgmd phenotype	34	add_hgmdphenotype
101	Can change hgmd phenotype	34	change_hgmdphenotype
102	Can delete hgmd phenotype	34	delete_hgmdphenotype
103	Can add cgd condition	35	add_cgdcondition
104	Can change cgd condition	35	change_cgdcondition
105	Can delete cgd condition	35	delete_cgdcondition
106	Can add cgd entry	36	add_cgdentry
107	Can change cgd entry	36	change_cgdentry
108	Can delete cgd entry	36	delete_cgdentry
109	Can add gene	37	add_gene
110	Can change gene	37	change_gene
111	Can delete gene	37	delete_gene
112	Can add gene category	38	add_genecategory
113	Can change gene category	38	change_genecategory
114	Can delete gene category	38	delete_genecategory
115	Can add gene group	39	add_genegroup
116	Can change gene group	39	change_genegroup
117	Can delete gene group	39	delete_genegroup
118	Can add gene list	40	add_genelist
119	Can change gene list	40	change_genelist
120	Can delete gene list	40	delete_genelist
121	Can add go term	41	add_goterm
122	Can change go term	41	change_goterm
123	Can delete go term	41	delete_goterm
124	Can add intervention	42	add_intervention
125	Can change intervention	42	change_intervention
126	Can delete intervention	42	delete_intervention
127	Can add manifestation	43	add_manifestation
128	Can change manifestation	43	change_manifestation
129	Can delete manifestation	43	delete_manifestation
130	Can add membership	44	add_membership
131	Can change membership	44	change_membership
132	Can delete membership	44	delete_membership
133	Can add case	45	add_case
134	Can change case	45	change_case
135	Can delete case	45	delete_case
136	Can add filter analysis	46	add_filteranalysis
137	Can change filter analysis	46	change_filteranalysis
138	Can delete filter analysis	46	delete_filteranalysis
139	Can add family filter analysis	47	add_familyfilteranalysis
140	Can change family filter analysis	47	change_familyfilteranalysis
141	Can delete family filter analysis	47	delete_familyfilteranalysis
142	Can add filter config	48	add_filterconfig
143	Can change filter config	48	change_filterconfig
144	Can delete filter config	48	delete_filterconfig
145	Can add pathway	49	add_pathway
146	Can change pathway	49	change_pathway
147	Can delete pathway	49	delete_pathway
148	Can add vari snp	50	add_varisnp
149	Can change vari snp	50	change_varisnp
150	Can delete vari snp	50	delete_varisnp
151	Can add project	51	add_project
152	Can change project	51	change_project
153	Can delete project	51	delete_project
154	Can add file	52	add_file
155	Can change file	52	change_file
156	Can delete file	52	delete_file
157	Can add s3 credential	53	add_s3credential
158	Can change s3 credential	53	change_s3credential
159	Can delete s3 credential	53	delete_s3credential
\.


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: raony
--

SELECT pg_catalog.setval('auth_permission_id_seq', 159, true);


--
-- Data for Name: auth_user; Type: TABLE DATA; Schema: public; Owner: raony
--

COPY auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) FROM stdin;
\.


--
-- Data for Name: auth_user_groups; Type: TABLE DATA; Schema: public; Owner: raony
--

COPY auth_user_groups (id, user_id, group_id) FROM stdin;
\.


--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: raony
--

SELECT pg_catalog.setval('auth_user_groups_id_seq', 1, false);


--
-- Name: auth_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: raony
--

SELECT pg_catalog.setval('auth_user_id_seq', 1, false);


--
-- Data for Name: auth_user_user_permissions; Type: TABLE DATA; Schema: public; Owner: raony
--

COPY auth_user_user_permissions (id, user_id, permission_id) FROM stdin;
\.


--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: raony
--

SELECT pg_catalog.setval('auth_user_user_permissions_id_seq', 1, false);


--
-- Data for Name: cases_case; Type: TABLE DATA; Schema: public; Owner: raony
--

COPY cases_case (id, status, name, description, father_id, mother_id, user_id) FROM stdin;
\.


--
-- Data for Name: cases_case_case_groups; Type: TABLE DATA; Schema: public; Owner: raony
--

COPY cases_case_case_groups (id, case_id, group_id) FROM stdin;
\.


--
-- Name: cases_case_case_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: raony
--

SELECT pg_catalog.setval('cases_case_case_groups_id_seq', 1, false);


--
-- Data for Name: cases_case_cases; Type: TABLE DATA; Schema: public; Owner: raony
--

COPY cases_case_cases (id, case_id, individual_id) FROM stdin;
\.


--
-- Name: cases_case_cases_id_seq; Type: SEQUENCE SET; Schema: public; Owner: raony
--

SELECT pg_catalog.setval('cases_case_cases_id_seq', 1, false);


--
-- Data for Name: cases_case_children; Type: TABLE DATA; Schema: public; Owner: raony
--

COPY cases_case_children (id, case_id, individual_id) FROM stdin;
\.


--
-- Name: cases_case_children_id_seq; Type: SEQUENCE SET; Schema: public; Owner: raony
--

SELECT pg_catalog.setval('cases_case_children_id_seq', 1, false);


--
-- Data for Name: cases_case_control_groups; Type: TABLE DATA; Schema: public; Owner: raony
--

COPY cases_case_control_groups (id, case_id, group_id) FROM stdin;
\.


--
-- Name: cases_case_control_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: raony
--

SELECT pg_catalog.setval('cases_case_control_groups_id_seq', 1, false);


--
-- Data for Name: cases_case_controls; Type: TABLE DATA; Schema: public; Owner: raony
--

COPY cases_case_controls (id, case_id, individual_id) FROM stdin;
\.


--
-- Name: cases_case_controls_id_seq; Type: SEQUENCE SET; Schema: public; Owner: raony
--

SELECT pg_catalog.setval('cases_case_controls_id_seq', 1, false);


--
-- Name: cases_case_id_seq; Type: SEQUENCE SET; Schema: public; Owner: raony
--

SELECT pg_catalog.setval('cases_case_id_seq', 1, false);


--
-- Data for Name: cases_case_shared_with_groups; Type: TABLE DATA; Schema: public; Owner: raony
--

COPY cases_case_shared_with_groups (id, case_id, group_id) FROM stdin;
\.


--
-- Name: cases_case_shared_with_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: raony
--

SELECT pg_catalog.setval('cases_case_shared_with_groups_id_seq', 1, false);


--
-- Data for Name: cases_case_shared_with_users; Type: TABLE DATA; Schema: public; Owner: raony
--

COPY cases_case_shared_with_users (id, case_id, user_id) FROM stdin;
\.


--
-- Name: cases_case_shared_with_users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: raony
--

SELECT pg_catalog.setval('cases_case_shared_with_users_id_seq', 1, false);


--
-- Data for Name: celery_taskmeta; Type: TABLE DATA; Schema: public; Owner: raony
--

COPY celery_taskmeta (id, task_id, status, result, date_done, traceback, hidden, meta) FROM stdin;
\.


--
-- Name: celery_taskmeta_id_seq; Type: SEQUENCE SET; Schema: public; Owner: raony
--

SELECT pg_catalog.setval('celery_taskmeta_id_seq', 1, false);


--
-- Data for Name: celery_tasksetmeta; Type: TABLE DATA; Schema: public; Owner: raony
--

COPY celery_tasksetmeta (id, taskset_id, result, date_done, hidden) FROM stdin;
\.


--
-- Name: celery_tasksetmeta_id_seq; Type: SEQUENCE SET; Schema: public; Owner: raony
--

SELECT pg_catalog.setval('celery_tasksetmeta_id_seq', 1, false);


--
-- Data for Name: diseases_disease; Type: TABLE DATA; Schema: public; Owner: raony
--

COPY diseases_disease (id, name, omim_id, chr_location, gene_names) FROM stdin;
\.


--
-- Name: diseases_disease_id_seq; Type: SEQUENCE SET; Schema: public; Owner: raony
--

SELECT pg_catalog.setval('diseases_disease_id_seq', 1, false);


--
-- Data for Name: diseases_gene; Type: TABLE DATA; Schema: public; Owner: raony
--

COPY diseases_gene (id, official_name, chromossome, names, strand, chr_location, transcription_start, transcription_end, cds_start, cds_end, exons_count, exons_start, exons_end) FROM stdin;
\.


--
-- Data for Name: diseases_gene_diseases; Type: TABLE DATA; Schema: public; Owner: raony
--

COPY diseases_gene_diseases (id, gene_id, disease_id) FROM stdin;
\.


--
-- Name: diseases_gene_diseases_id_seq; Type: SEQUENCE SET; Schema: public; Owner: raony
--

SELECT pg_catalog.setval('diseases_gene_diseases_id_seq', 1, false);


--
-- Name: diseases_gene_id_seq; Type: SEQUENCE SET; Schema: public; Owner: raony
--

SELECT pg_catalog.setval('diseases_gene_id_seq', 1, false);


--
-- Data for Name: diseases_hgmdgene; Type: TABLE DATA; Schema: public; Owner: raony
--

COPY diseases_hgmdgene (id, symbol, aliases, description, description_aliases, location, n_mutations) FROM stdin;
\.


--
-- Data for Name: diseases_hgmdgene_diseases; Type: TABLE DATA; Schema: public; Owner: raony
--

COPY diseases_hgmdgene_diseases (id, hgmdgene_id, hgmdphenotype_id) FROM stdin;
\.


--
-- Name: diseases_hgmdgene_diseases_id_seq; Type: SEQUENCE SET; Schema: public; Owner: raony
--

SELECT pg_catalog.setval('diseases_hgmdgene_diseases_id_seq', 1, false);


--
-- Name: diseases_hgmdgene_id_seq; Type: SEQUENCE SET; Schema: public; Owner: raony
--

SELECT pg_catalog.setval('diseases_hgmdgene_id_seq', 1, false);


--
-- Data for Name: diseases_hgmdmutation; Type: TABLE DATA; Schema: public; Owner: raony
--

COPY diseases_hgmdmutation (id, mutation_type, acession, reference, extras, rsid, dm_mutation, coordinate, chromossome, "position", codon_change, aa_change, hgvs_nucleotide, hgvs_protein, splicing_mutation, regulatory_sequence, deletion_sequence, insertion_sequence, dna_level, description, insertion_duplication, amplified_sequence, location, normal_range, pathological_range, gene_id, phenotype_id) FROM stdin;
\.


--
-- Name: diseases_hgmdmutation_id_seq; Type: SEQUENCE SET; Schema: public; Owner: raony
--

SELECT pg_catalog.setval('diseases_hgmdmutation_id_seq', 1, false);


--
-- Data for Name: diseases_hgmdphenotype; Type: TABLE DATA; Schema: public; Owner: raony
--

COPY diseases_hgmdphenotype (id, name) FROM stdin;
\.


--
-- Name: diseases_hgmdphenotype_id_seq; Type: SEQUENCE SET; Schema: public; Owner: raony
--

SELECT pg_catalog.setval('diseases_hgmdphenotype_id_seq', 1, false);


--
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: raony
--

COPY django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) FROM stdin;
\.


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: raony
--

SELECT pg_catalog.setval('django_admin_log_id_seq', 1, false);


--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: raony
--

COPY django_content_type (id, app_label, model) FROM stdin;
1	admin	logentry
2	auth	permission
3	auth	group
4	auth	user
5	contenttypes	contenttype
6	sessions	session
7	sites	site
8	account	emailaddress
9	account	emailconfirmation
10	socialaccount	socialaccount
11	socialaccount	socialapp
12	socialaccount	socialtoken
13	djcelery	crontabschedule
14	djcelery	intervalschedule
15	djcelery	periodictask
16	djcelery	periodictasks
17	djcelery	taskmeta
18	djcelery	tasksetmeta
19	djcelery	taskstate
20	djcelery	workerstate
21	kombu_transport_django	message
22	kombu_transport_django	queue
23	individuals	controlgroup
24	individuals	controlvariant
25	individuals	group
26	individuals	individual
27	individuals	usergroup
28	variants	variant
29	variants	variantannotation
30	diseases	disease
31	diseases	gene
32	diseases	hgmdgene
33	diseases	hgmdmutation
34	diseases	hgmdphenotype
35	genes	cgdcondition
36	genes	cgdentry
37	genes	gene
38	genes	genecategory
39	genes	genegroup
40	genes	genelist
41	genes	goterm
42	genes	intervention
43	genes	manifestation
44	genes	membership
45	cases	case
46	filter_analysis	filteranalysis
47	filter_analysis	familyfilteranalysis
48	filter_analysis	filterconfig
49	pathway_analysis	pathway
50	databases	varisnp
51	projects	project
52	files	file
53	files	s3credential
\.


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: raony
--

SELECT pg_catalog.setval('django_content_type_id_seq', 53, true);


--
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: raony
--

COPY django_migrations (id, app, name, applied) FROM stdin;
1	contenttypes	0001_initial	2017-10-06 00:13:23.366455+01
2	auth	0001_initial	2017-10-06 00:13:24.07614+01
3	account	0001_initial	2017-10-06 00:13:24.409298+01
4	account	0002_email_max_length	2017-10-06 00:13:24.450864+01
5	admin	0001_initial	2017-10-06 00:13:24.642929+01
6	admin	0002_logentry_remove_auto_add	2017-10-06 00:13:24.683759+01
7	contenttypes	0002_remove_content_type_name	2017-10-06 00:13:24.741436+01
8	auth	0002_alter_permission_name_max_length	2017-10-06 00:13:24.757994+01
9	auth	0003_alter_user_email_max_length	2017-10-06 00:13:24.783135+01
10	auth	0004_alter_user_username_opts	2017-10-06 00:13:24.798454+01
11	auth	0005_alter_user_last_login_null	2017-10-06 00:13:24.825995+01
12	auth	0006_require_contenttypes_0002	2017-10-06 00:13:24.834664+01
13	auth	0007_alter_validators_add_error_messages	2017-10-06 00:13:24.867879+01
14	auth	0008_alter_user_username_max_length	2017-10-06 00:13:24.934635+01
15	individuals	0001_initial	2017-10-06 00:13:26.104093+01
16	cases	0001_initial	2017-10-06 00:13:27.289211+01
17	diseases	0001_initial	2017-10-06 00:13:28.073009+01
18	djcelery	0001_initial	2017-10-06 00:13:29.349249+01
19	files	0001_initial	2017-10-06 00:13:29.523949+01
20	genes	0001_initial	2017-10-06 00:13:31.452316+01
21	kombu_transport_django	0001_initial	2017-10-06 00:13:31.73519+01
22	projects	0001_initial	2017-10-06 00:13:32.47806+01
23	sessions	0001_initial	2017-10-06 00:13:32.644162+01
24	sites	0001_initial	2017-10-06 00:13:32.71168+01
25	sites	0002_alter_domain_unique	2017-10-06 00:13:32.819928+01
26	socialaccount	0001_initial	2017-10-06 00:13:33.487742+01
27	socialaccount	0002_token_max_lengths	2017-10-06 00:13:33.585351+01
28	socialaccount	0003_extra_data_default_dict	2017-10-06 00:13:33.602053+01
29	variants	0001_initial	2017-10-06 00:13:43.459894+01
30	variants	0002_auto_20171005_2251	2017-10-06 00:13:43.481278+01
\.


--
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: raony
--

SELECT pg_catalog.setval('django_migrations_id_seq', 30, true);


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: raony
--

COPY django_session (session_key, session_data, expire_date) FROM stdin;
\.


--
-- Data for Name: django_site; Type: TABLE DATA; Schema: public; Owner: raony
--

COPY django_site (id, domain, name) FROM stdin;
1	example.com	example.com
\.


--
-- Name: django_site_id_seq; Type: SEQUENCE SET; Schema: public; Owner: raony
--

SELECT pg_catalog.setval('django_site_id_seq', 1, true);


--
-- Data for Name: djcelery_crontabschedule; Type: TABLE DATA; Schema: public; Owner: raony
--

COPY djcelery_crontabschedule (id, minute, hour, day_of_week, day_of_month, month_of_year) FROM stdin;
\.


--
-- Name: djcelery_crontabschedule_id_seq; Type: SEQUENCE SET; Schema: public; Owner: raony
--

SELECT pg_catalog.setval('djcelery_crontabschedule_id_seq', 1, false);


--
-- Data for Name: djcelery_intervalschedule; Type: TABLE DATA; Schema: public; Owner: raony
--

COPY djcelery_intervalschedule (id, every, period) FROM stdin;
\.


--
-- Name: djcelery_intervalschedule_id_seq; Type: SEQUENCE SET; Schema: public; Owner: raony
--

SELECT pg_catalog.setval('djcelery_intervalschedule_id_seq', 1, false);


--
-- Data for Name: djcelery_periodictask; Type: TABLE DATA; Schema: public; Owner: raony
--

COPY djcelery_periodictask (id, name, task, args, kwargs, queue, exchange, routing_key, expires, enabled, last_run_at, total_run_count, date_changed, description, crontab_id, interval_id) FROM stdin;
\.


--
-- Name: djcelery_periodictask_id_seq; Type: SEQUENCE SET; Schema: public; Owner: raony
--

SELECT pg_catalog.setval('djcelery_periodictask_id_seq', 1, false);


--
-- Data for Name: djcelery_periodictasks; Type: TABLE DATA; Schema: public; Owner: raony
--

COPY djcelery_periodictasks (ident, last_update) FROM stdin;
\.


--
-- Data for Name: djcelery_taskstate; Type: TABLE DATA; Schema: public; Owner: raony
--

COPY djcelery_taskstate (id, state, task_id, name, tstamp, args, kwargs, eta, expires, result, traceback, runtime, retries, hidden, worker_id) FROM stdin;
\.


--
-- Name: djcelery_taskstate_id_seq; Type: SEQUENCE SET; Schema: public; Owner: raony
--

SELECT pg_catalog.setval('djcelery_taskstate_id_seq', 1, false);


--
-- Data for Name: djcelery_workerstate; Type: TABLE DATA; Schema: public; Owner: raony
--

COPY djcelery_workerstate (id, hostname, last_heartbeat) FROM stdin;
\.


--
-- Name: djcelery_workerstate_id_seq; Type: SEQUENCE SET; Schema: public; Owner: raony
--

SELECT pg_catalog.setval('djcelery_workerstate_id_seq', 1, false);


--
-- Data for Name: djkombu_message; Type: TABLE DATA; Schema: public; Owner: raony
--

COPY djkombu_message (id, visible, sent_at, payload, queue_id) FROM stdin;
\.


--
-- Name: djkombu_message_id_seq; Type: SEQUENCE SET; Schema: public; Owner: raony
--

SELECT pg_catalog.setval('djkombu_message_id_seq', 1, false);


--
-- Data for Name: djkombu_queue; Type: TABLE DATA; Schema: public; Owner: raony
--

COPY djkombu_queue (id, name) FROM stdin;
\.


--
-- Name: djkombu_queue_id_seq; Type: SEQUENCE SET; Schema: public; Owner: raony
--

SELECT pg_catalog.setval('djkombu_queue_id_seq', 1, false);


--
-- Data for Name: files_file; Type: TABLE DATA; Schema: public; Owner: raony
--

COPY files_file (id, name, size, last_modified, file_type, location, local_file, status, md5, creation_date, modified_date) FROM stdin;
\.


--
-- Name: files_file_id_seq; Type: SEQUENCE SET; Schema: public; Owner: raony
--

SELECT pg_catalog.setval('files_file_id_seq', 1, false);


--
-- Data for Name: files_s3credential; Type: TABLE DATA; Schema: public; Owner: raony
--

COPY files_s3credential (id, name, access_key, secret_key, buckets, exclude_paths, exclude_files) FROM stdin;
\.


--
-- Name: files_s3credential_id_seq; Type: SEQUENCE SET; Schema: public; Owner: raony
--

SELECT pg_catalog.setval('files_s3credential_id_seq', 1, false);


--
-- Data for Name: genes_cgdcondition; Type: TABLE DATA; Schema: public; Owner: raony
--

COPY genes_cgdcondition (id, name) FROM stdin;
\.


--
-- Name: genes_cgdcondition_id_seq; Type: SEQUENCE SET; Schema: public; Owner: raony
--

SELECT pg_catalog.setval('genes_cgdcondition_id_seq', 1, false);


--
-- Data for Name: genes_cgdentry; Type: TABLE DATA; Schema: public; Owner: raony
--

COPY genes_cgdentry (id, "GENE", "HGNC_ID", "ENTREZ_GENE_ID", "INHERITANCE", "AGE_GROUP", "ALLELIC_CONDITIONS", "COMMENTS", "INTERVENTION_RATIONALE", "REFERENCES") FROM stdin;
\.


--
-- Data for Name: genes_cgdentry_CONDITIONS; Type: TABLE DATA; Schema: public; Owner: raony
--

COPY "genes_cgdentry_CONDITIONS" (id, cgdentry_id, cgdcondition_id) FROM stdin;
\.


--
-- Name: genes_cgdentry_CONDITIONS_id_seq; Type: SEQUENCE SET; Schema: public; Owner: raony
--

SELECT pg_catalog.setval('"genes_cgdentry_CONDITIONS_id_seq"', 1, false);


--
-- Data for Name: genes_cgdentry_INTERVENTION_CATEGORIES; Type: TABLE DATA; Schema: public; Owner: raony
--

COPY "genes_cgdentry_INTERVENTION_CATEGORIES" (id, cgdentry_id, intervention_id) FROM stdin;
\.


--
-- Name: genes_cgdentry_INTERVENTION_CATEGORIES_id_seq; Type: SEQUENCE SET; Schema: public; Owner: raony
--

SELECT pg_catalog.setval('"genes_cgdentry_INTERVENTION_CATEGORIES_id_seq"', 1, false);


--
-- Data for Name: genes_cgdentry_MANIFESTATION_CATEGORIES; Type: TABLE DATA; Schema: public; Owner: raony
--

COPY "genes_cgdentry_MANIFESTATION_CATEGORIES" (id, cgdentry_id, manifestation_id) FROM stdin;
\.


--
-- Name: genes_cgdentry_MANIFESTATION_CATEGORIES_id_seq; Type: SEQUENCE SET; Schema: public; Owner: raony
--

SELECT pg_catalog.setval('"genes_cgdentry_MANIFESTATION_CATEGORIES_id_seq"', 1, false);


--
-- Name: genes_cgdentry_id_seq; Type: SEQUENCE SET; Schema: public; Owner: raony
--

SELECT pg_catalog.setval('genes_cgdentry_id_seq', 1, false);


--
-- Data for Name: genes_gene; Type: TABLE DATA; Schema: public; Owner: raony
--

COPY genes_gene (id, hgnc_id, symbol, name, locus_group, locus_type, status, location, location_sortable, alias_symbol, alias_name, prev_symbol, prev_name, gene_family, gene_family_id, date_approved_reserved, date_symbol_changed, date_name_changed, date_modified, entrez_id, ensembl_gene_id, vega_id, ucsc_id, ena, refseq_accession, ccds_id, uniprot_ids, pubmed_id, mgd_id, rgd_id, lsdb, cosmic, omim_id, mirbase, homeodb, snornabase, bioparadigms_slc, orphanet, pseudogene_org, horde_id, merops, imgt, iuphar, kznf_gene_catalog, mamit_trnadb, cd, lncrnadb, enzyme_id, intermediate_filament_db) FROM stdin;
\.


--
-- Data for Name: genes_gene_diseases; Type: TABLE DATA; Schema: public; Owner: raony
--

COPY genes_gene_diseases (id, gene_id, disease_id) FROM stdin;
\.


--
-- Name: genes_gene_diseases_id_seq; Type: SEQUENCE SET; Schema: public; Owner: raony
--

SELECT pg_catalog.setval('genes_gene_diseases_id_seq', 1, false);


--
-- Name: genes_gene_id_seq; Type: SEQUENCE SET; Schema: public; Owner: raony
--

SELECT pg_catalog.setval('genes_gene_id_seq', 1, false);


--
-- Data for Name: genes_genecategory; Type: TABLE DATA; Schema: public; Owner: raony
--

COPY genes_genecategory (id, domain, name, go, definition) FROM stdin;
\.


--
-- Data for Name: genes_genecategory_genes; Type: TABLE DATA; Schema: public; Owner: raony
--

COPY genes_genecategory_genes (id, genecategory_id, gene_id) FROM stdin;
\.


--
-- Name: genes_genecategory_genes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: raony
--

SELECT pg_catalog.setval('genes_genecategory_genes_id_seq', 1, false);


--
-- Name: genes_genecategory_id_seq; Type: SEQUENCE SET; Schema: public; Owner: raony
--

SELECT pg_catalog.setval('genes_genecategory_id_seq', 1, false);


--
-- Data for Name: genes_genegroup; Type: TABLE DATA; Schema: public; Owner: raony
--

COPY genes_genegroup (id, name, genes) FROM stdin;
\.


--
-- Name: genes_genegroup_id_seq; Type: SEQUENCE SET; Schema: public; Owner: raony
--

SELECT pg_catalog.setval('genes_genegroup_id_seq', 1, false);


--
-- Data for Name: genes_genelist; Type: TABLE DATA; Schema: public; Owner: raony
--

COPY genes_genelist (id, name, genes, user_id) FROM stdin;
\.


--
-- Name: genes_genelist_id_seq; Type: SEQUENCE SET; Schema: public; Owner: raony
--

SELECT pg_catalog.setval('genes_genelist_id_seq', 1, false);


--
-- Data for Name: genes_goterm; Type: TABLE DATA; Schema: public; Owner: raony
--

COPY genes_goterm (id, goid, name, namespace, level, is_obsolete, alt_ids) FROM stdin;
\.


--
-- Data for Name: genes_goterm_children; Type: TABLE DATA; Schema: public; Owner: raony
--

COPY genes_goterm_children (id, from_goterm_id, to_goterm_id) FROM stdin;
\.


--
-- Name: genes_goterm_children_id_seq; Type: SEQUENCE SET; Schema: public; Owner: raony
--

SELECT pg_catalog.setval('genes_goterm_children_id_seq', 1, false);


--
-- Name: genes_goterm_id_seq; Type: SEQUENCE SET; Schema: public; Owner: raony
--

SELECT pg_catalog.setval('genes_goterm_id_seq', 1, false);


--
-- Data for Name: genes_goterm_parents; Type: TABLE DATA; Schema: public; Owner: raony
--

COPY genes_goterm_parents (id, from_goterm_id, to_goterm_id) FROM stdin;
\.


--
-- Name: genes_goterm_parents_id_seq; Type: SEQUENCE SET; Schema: public; Owner: raony
--

SELECT pg_catalog.setval('genes_goterm_parents_id_seq', 1, false);


--
-- Data for Name: genes_intervention; Type: TABLE DATA; Schema: public; Owner: raony
--

COPY genes_intervention (id, name) FROM stdin;
\.


--
-- Name: genes_intervention_id_seq; Type: SEQUENCE SET; Schema: public; Owner: raony
--

SELECT pg_catalog.setval('genes_intervention_id_seq', 1, false);


--
-- Data for Name: genes_manifestation; Type: TABLE DATA; Schema: public; Owner: raony
--

COPY genes_manifestation (id, name) FROM stdin;
\.


--
-- Name: genes_manifestation_id_seq; Type: SEQUENCE SET; Schema: public; Owner: raony
--

SELECT pg_catalog.setval('genes_manifestation_id_seq', 1, false);


--
-- Data for Name: genes_membership; Type: TABLE DATA; Schema: public; Owner: raony
--

COPY genes_membership (id, gene_id, group_id) FROM stdin;
\.


--
-- Name: genes_membership_id_seq; Type: SEQUENCE SET; Schema: public; Owner: raony
--

SELECT pg_catalog.setval('genes_membership_id_seq', 1, false);


--
-- Data for Name: individuals_controlgroup; Type: TABLE DATA; Schema: public; Owner: raony
--

COPY individuals_controlgroup (id, name, vcf_file) FROM stdin;
\.


--
-- Name: individuals_controlgroup_id_seq; Type: SEQUENCE SET; Schema: public; Owner: raony
--

SELECT pg_catalog.setval('individuals_controlgroup_id_seq', 1, false);


--
-- Data for Name: individuals_controlvariant; Type: TABLE DATA; Schema: public; Owner: raony
--

COPY individuals_controlvariant (id, index, controlgroup_id) FROM stdin;
\.


--
-- Name: individuals_controlvariant_id_seq; Type: SEQUENCE SET; Schema: public; Owner: raony
--

SELECT pg_catalog.setval('individuals_controlvariant_id_seq', 1, false);


--
-- Data for Name: individuals_group; Type: TABLE DATA; Schema: public; Owner: raony
--

COPY individuals_group (id, name) FROM stdin;
\.


--
-- Name: individuals_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: raony
--

SELECT pg_catalog.setval('individuals_group_id_seq', 1, false);


--
-- Data for Name: individuals_group_members; Type: TABLE DATA; Schema: public; Owner: raony
--

COPY individuals_group_members (id, group_id, individual_id) FROM stdin;
\.


--
-- Name: individuals_group_members_id_seq; Type: SEQUENCE SET; Schema: public; Owner: raony
--

SELECT pg_catalog.setval('individuals_group_members_id_seq', 1, false);


--
-- Data for Name: individuals_individual; Type: TABLE DATA; Schema: public; Owner: raony
--

COPY individuals_individual (id, name, is_featured, is_public, vcf_file, vcf_header, status, n_variants, n_lines, creation_date, modified_date, annotation_time, insertion_time, user_id) FROM stdin;
\.


--
-- Name: individuals_individual_id_seq; Type: SEQUENCE SET; Schema: public; Owner: raony
--

SELECT pg_catalog.setval('individuals_individual_id_seq', 1, false);


--
-- Data for Name: individuals_individual_shared_with_groups; Type: TABLE DATA; Schema: public; Owner: raony
--

COPY individuals_individual_shared_with_groups (id, individual_id, usergroup_id) FROM stdin;
\.


--
-- Name: individuals_individual_shared_with_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: raony
--

SELECT pg_catalog.setval('individuals_individual_shared_with_groups_id_seq', 1, false);


--
-- Data for Name: individuals_individual_shared_with_users; Type: TABLE DATA; Schema: public; Owner: raony
--

COPY individuals_individual_shared_with_users (id, individual_id, user_id) FROM stdin;
\.


--
-- Name: individuals_individual_shared_with_users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: raony
--

SELECT pg_catalog.setval('individuals_individual_shared_with_users_id_seq', 1, false);


--
-- Data for Name: individuals_usergroup; Type: TABLE DATA; Schema: public; Owner: raony
--

COPY individuals_usergroup (id, name) FROM stdin;
\.


--
-- Name: individuals_usergroup_id_seq; Type: SEQUENCE SET; Schema: public; Owner: raony
--

SELECT pg_catalog.setval('individuals_usergroup_id_seq', 1, false);


--
-- Data for Name: individuals_usergroup_members; Type: TABLE DATA; Schema: public; Owner: raony
--

COPY individuals_usergroup_members (id, usergroup_id, user_id) FROM stdin;
\.


--
-- Name: individuals_usergroup_members_id_seq; Type: SEQUENCE SET; Schema: public; Owner: raony
--

SELECT pg_catalog.setval('individuals_usergroup_members_id_seq', 1, false);


--
-- Data for Name: projects_project; Type: TABLE DATA; Schema: public; Owner: raony
--

COPY projects_project (id, name, description, is_public, status, creation_date, modified_date, user_id) FROM stdin;
\.


--
-- Data for Name: projects_project_files; Type: TABLE DATA; Schema: public; Owner: raony
--

COPY projects_project_files (id, project_id, file_id) FROM stdin;
\.


--
-- Name: projects_project_files_id_seq; Type: SEQUENCE SET; Schema: public; Owner: raony
--

SELECT pg_catalog.setval('projects_project_files_id_seq', 1, false);


--
-- Data for Name: projects_project_groups; Type: TABLE DATA; Schema: public; Owner: raony
--

COPY projects_project_groups (id, project_id, group_id) FROM stdin;
\.


--
-- Name: projects_project_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: raony
--

SELECT pg_catalog.setval('projects_project_groups_id_seq', 1, false);


--
-- Name: projects_project_id_seq; Type: SEQUENCE SET; Schema: public; Owner: raony
--

SELECT pg_catalog.setval('projects_project_id_seq', 1, false);


--
-- Data for Name: projects_project_individuals; Type: TABLE DATA; Schema: public; Owner: raony
--

COPY projects_project_individuals (id, project_id, individual_id) FROM stdin;
\.


--
-- Name: projects_project_individuals_id_seq; Type: SEQUENCE SET; Schema: public; Owner: raony
--

SELECT pg_catalog.setval('projects_project_individuals_id_seq', 1, false);


--
-- Data for Name: projects_project_members; Type: TABLE DATA; Schema: public; Owner: raony
--

COPY projects_project_members (id, project_id, user_id) FROM stdin;
\.


--
-- Name: projects_project_members_id_seq; Type: SEQUENCE SET; Schema: public; Owner: raony
--

SELECT pg_catalog.setval('projects_project_members_id_seq', 1, false);


--
-- Data for Name: socialaccount_socialaccount; Type: TABLE DATA; Schema: public; Owner: raony
--

COPY socialaccount_socialaccount (id, provider, uid, last_login, date_joined, extra_data, user_id) FROM stdin;
\.


--
-- Name: socialaccount_socialaccount_id_seq; Type: SEQUENCE SET; Schema: public; Owner: raony
--

SELECT pg_catalog.setval('socialaccount_socialaccount_id_seq', 1, false);


--
-- Data for Name: socialaccount_socialapp; Type: TABLE DATA; Schema: public; Owner: raony
--

COPY socialaccount_socialapp (id, provider, name, client_id, secret, key) FROM stdin;
\.


--
-- Name: socialaccount_socialapp_id_seq; Type: SEQUENCE SET; Schema: public; Owner: raony
--

SELECT pg_catalog.setval('socialaccount_socialapp_id_seq', 1, false);


--
-- Data for Name: socialaccount_socialapp_sites; Type: TABLE DATA; Schema: public; Owner: raony
--

COPY socialaccount_socialapp_sites (id, socialapp_id, site_id) FROM stdin;
\.


--
-- Name: socialaccount_socialapp_sites_id_seq; Type: SEQUENCE SET; Schema: public; Owner: raony
--

SELECT pg_catalog.setval('socialaccount_socialapp_sites_id_seq', 1, false);


--
-- Data for Name: socialaccount_socialtoken; Type: TABLE DATA; Schema: public; Owner: raony
--

COPY socialaccount_socialtoken (id, token, token_secret, expires_at, account_id, app_id) FROM stdin;
\.


--
-- Name: socialaccount_socialtoken_id_seq; Type: SEQUENCE SET; Schema: public; Owner: raony
--

SELECT pg_catalog.setval('socialaccount_socialtoken_id_seq', 1, false);


--
-- Data for Name: variants_variant; Type: TABLE DATA; Schema: public; Owner: raony
--

COPY variants_variant (id, chr, pos, index) FROM stdin;
\.


--
-- Name: variants_variant_id_seq; Type: SEQUENCE SET; Schema: public; Owner: raony
--

SELECT pg_catalog.setval('variants_variant_id_seq', 1, false);


--
-- Data for Name: variants_variantannotation; Type: TABLE DATA; Schema: public; Owner: raony
--

COPY variants_variantannotation (id, variant_id, ref, alt, qual, filter, info, format, genotype_col, genotype, read_depth, gene, mutation_type, vartype, genomes1k_maf, dbsnp_maf, esp_maf, dbsnp_build, sift, sift_pred, polyphen2, polyphen2_pred, condel, condel_pred, dann, cadd, hi_index_str, hi_index, hi_index_perc, is_at_omim, is_at_hgmd, hgmd_entries, snpeff_effect, snpeff_impact, snpeff_func_class, snpeff_codon_change, snpeff_aa_change, snpeff_gene_name, snpeff_biotype, snpeff_gene_coding, snpeff_transcript_id, snpeff_exon_rank, vep_allele, vep_gene, vep_feature, vep_feature_type, vep_consequence, vep_cdna_position, vep_cds_position, vep_protein_position, vep_amino_acids, vep_codons, vep_existing_variation, vep_distance, vep_strand, vep_symbol, vep_symbol_source, vep_sift, vep_polyphen, vep_condel, "ensembl_clin_HGMD", "clinvar_CLNSRC", "SIFT_score", "SIFT_converted_rankscore", "Uniprot_acc_Polyphen2", "Uniprot_id_Polyphen2", "Uniprot_aapos_Polyphen2", "Polyphen2_HDIV_score", "Polyphen2_HDIV_rankscore", "Polyphen2_HDIV_pred", "Polyphen2_HVAR_score", "Polyphen2_HVAR_rankscore", "Polyphen2_HVAR_pred", "LRT_score", "LRT_converted_rankscore", "LRT_pred", "LRT_Omega", "MutationTaster_score", "MutationTaster_converted_rankscore", "MutationTaster_pred", "MutationTaster_model", "MutationTaster_AAE", "MutationAssessor_UniprotID", "MutationAssessor_variant", "MutationAssessor_score", "MutationAssessor_rankscore", "MutationAssessor_pred", "FATHMM_score", "FATHMM_converted_rankscore", "FATHMM_pred", "PROVEAN_score", "PROVEAN_converted_rankscore", "PROVEAN_pred", "Transcript_id_VEST3", "Transcript_var_VEST3", "VEST3_score", "VEST3_rankscore", "MetaSVM_score", "MetaSVM_rankscore", "MetaSVM_pred", "MetaLR_score", "MetaLR_rankscore", "MetaLR_pred", "Reliability_index", "CADD_raw", "CADD_raw_rankscore", "CADD_phred", "DANN_score", "DANN_rankscore", "fathmm_MKL_coding_score", "fathmm_MKL_coding_rankscore", "fathmm_MKL_coding_pred", "fathmm_MKL_coding_group", "Eigen_raw", "Eigen_phred", "Eigen_raw_rankscore", "Eigen_PC_raw", "Eigen_PC_raw_rankscore", "GenoCanyon_score", "GenoCanyon_score_rankscore", "integrated_fitCons_score", "integrated_fitCons_rankscore", integrated_confidence_value, "GM12878_fitCons_score", "GM12878_fitCons_rankscore", "GM12878_confidence_value", "H1_hESC_fitCons_score", "H1_hESC_fitCons_rankscore", "H1_hESC_confidence_value", "HUVEC_fitCons_score", "HUVEC_fitCons_rankscore", "HUVEC_confidence_value", "GERP_NR", "GERP_RS", "GERP_RS_rankscore", "phyloP100way_vertebrate", "phyloP100way_vertebrate_rankscore", "phyloP20way_mammalian", "phyloP20way_mammalian_rankscore", "phastCons100way_vertebrate", "phastCons100way_vertebrate_rankscore", "phastCons20way_mammalian", "phastCons20way_mammalian_rankscore", "SiPhy_29way_pi", "SiPhy_29way_logOdds", "SiPhy_29way_logOdds_rankscore", clinvar_rs, clinvar_clnsig, clinvar_trait, clinvar_golden_stars, mcap_score, mcap_rankscore, mcap_pred, revel_score) FROM stdin;
\.


--
-- Name: variants_variantannotation_id_seq; Type: SEQUENCE SET; Schema: public; Owner: raony
--

SELECT pg_catalog.setval('variants_variantannotation_id_seq', 1, false);


--
-- Name: account_emailaddress account_emailaddress_email_key; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY account_emailaddress
    ADD CONSTRAINT account_emailaddress_email_key UNIQUE (email);


--
-- Name: account_emailaddress account_emailaddress_pkey; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY account_emailaddress
    ADD CONSTRAINT account_emailaddress_pkey PRIMARY KEY (id);


--
-- Name: account_emailconfirmation account_emailconfirmation_key_key; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY account_emailconfirmation
    ADD CONSTRAINT account_emailconfirmation_key_key UNIQUE (key);


--
-- Name: account_emailconfirmation account_emailconfirmation_pkey; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY account_emailconfirmation
    ADD CONSTRAINT account_emailconfirmation_pkey PRIMARY KEY (id);


--
-- Name: auth_group auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- Name: auth_group_permissions auth_group_permissions_group_id_permission_id_0cd325b0_uniq; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq UNIQUE (group_id, permission_id);


--
-- Name: auth_group_permissions auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_group auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_permission auth_permission_content_type_id_codename_01ab375a_uniq; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq UNIQUE (content_type_id, codename);


--
-- Name: auth_permission auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups auth_user_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups auth_user_groups_user_id_group_id_94350c0c_uniq; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_group_id_94350c0c_uniq UNIQUE (user_id, group_id);


--
-- Name: auth_user auth_user_pkey; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY auth_user
    ADD CONSTRAINT auth_user_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions auth_user_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions auth_user_user_permissions_user_id_permission_id_14a6b632_uniq; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_permission_id_14a6b632_uniq UNIQUE (user_id, permission_id);


--
-- Name: auth_user auth_user_username_key; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY auth_user
    ADD CONSTRAINT auth_user_username_key UNIQUE (username);


--
-- Name: cases_case_case_groups cases_case_case_groups_case_id_group_id_8e5152ba_uniq; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY cases_case_case_groups
    ADD CONSTRAINT cases_case_case_groups_case_id_group_id_8e5152ba_uniq UNIQUE (case_id, group_id);


--
-- Name: cases_case_case_groups cases_case_case_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY cases_case_case_groups
    ADD CONSTRAINT cases_case_case_groups_pkey PRIMARY KEY (id);


--
-- Name: cases_case_cases cases_case_cases_case_id_individual_id_58210e01_uniq; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY cases_case_cases
    ADD CONSTRAINT cases_case_cases_case_id_individual_id_58210e01_uniq UNIQUE (case_id, individual_id);


--
-- Name: cases_case_cases cases_case_cases_pkey; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY cases_case_cases
    ADD CONSTRAINT cases_case_cases_pkey PRIMARY KEY (id);


--
-- Name: cases_case_children cases_case_children_case_id_individual_id_412ee3c7_uniq; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY cases_case_children
    ADD CONSTRAINT cases_case_children_case_id_individual_id_412ee3c7_uniq UNIQUE (case_id, individual_id);


--
-- Name: cases_case_children cases_case_children_pkey; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY cases_case_children
    ADD CONSTRAINT cases_case_children_pkey PRIMARY KEY (id);


--
-- Name: cases_case_control_groups cases_case_control_groups_case_id_group_id_2f626389_uniq; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY cases_case_control_groups
    ADD CONSTRAINT cases_case_control_groups_case_id_group_id_2f626389_uniq UNIQUE (case_id, group_id);


--
-- Name: cases_case_control_groups cases_case_control_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY cases_case_control_groups
    ADD CONSTRAINT cases_case_control_groups_pkey PRIMARY KEY (id);


--
-- Name: cases_case_controls cases_case_controls_case_id_individual_id_cb1a4b10_uniq; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY cases_case_controls
    ADD CONSTRAINT cases_case_controls_case_id_individual_id_cb1a4b10_uniq UNIQUE (case_id, individual_id);


--
-- Name: cases_case_controls cases_case_controls_pkey; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY cases_case_controls
    ADD CONSTRAINT cases_case_controls_pkey PRIMARY KEY (id);


--
-- Name: cases_case cases_case_pkey; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY cases_case
    ADD CONSTRAINT cases_case_pkey PRIMARY KEY (id);


--
-- Name: cases_case_shared_with_groups cases_case_shared_with_groups_case_id_group_id_57b2dc94_uniq; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY cases_case_shared_with_groups
    ADD CONSTRAINT cases_case_shared_with_groups_case_id_group_id_57b2dc94_uniq UNIQUE (case_id, group_id);


--
-- Name: cases_case_shared_with_groups cases_case_shared_with_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY cases_case_shared_with_groups
    ADD CONSTRAINT cases_case_shared_with_groups_pkey PRIMARY KEY (id);


--
-- Name: cases_case_shared_with_users cases_case_shared_with_users_case_id_user_id_7a52821f_uniq; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY cases_case_shared_with_users
    ADD CONSTRAINT cases_case_shared_with_users_case_id_user_id_7a52821f_uniq UNIQUE (case_id, user_id);


--
-- Name: cases_case_shared_with_users cases_case_shared_with_users_pkey; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY cases_case_shared_with_users
    ADD CONSTRAINT cases_case_shared_with_users_pkey PRIMARY KEY (id);


--
-- Name: celery_taskmeta celery_taskmeta_pkey; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY celery_taskmeta
    ADD CONSTRAINT celery_taskmeta_pkey PRIMARY KEY (id);


--
-- Name: celery_taskmeta celery_taskmeta_task_id_key; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY celery_taskmeta
    ADD CONSTRAINT celery_taskmeta_task_id_key UNIQUE (task_id);


--
-- Name: celery_tasksetmeta celery_tasksetmeta_pkey; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY celery_tasksetmeta
    ADD CONSTRAINT celery_tasksetmeta_pkey PRIMARY KEY (id);


--
-- Name: celery_tasksetmeta celery_tasksetmeta_taskset_id_key; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY celery_tasksetmeta
    ADD CONSTRAINT celery_tasksetmeta_taskset_id_key UNIQUE (taskset_id);


--
-- Name: diseases_disease diseases_disease_pkey; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY diseases_disease
    ADD CONSTRAINT diseases_disease_pkey PRIMARY KEY (id);


--
-- Name: diseases_gene_diseases diseases_gene_diseases_gene_id_disease_id_3d27d696_uniq; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY diseases_gene_diseases
    ADD CONSTRAINT diseases_gene_diseases_gene_id_disease_id_3d27d696_uniq UNIQUE (gene_id, disease_id);


--
-- Name: diseases_gene_diseases diseases_gene_diseases_pkey; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY diseases_gene_diseases
    ADD CONSTRAINT diseases_gene_diseases_pkey PRIMARY KEY (id);


--
-- Name: diseases_gene diseases_gene_pkey; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY diseases_gene
    ADD CONSTRAINT diseases_gene_pkey PRIMARY KEY (id);


--
-- Name: diseases_hgmdgene_diseases diseases_hgmdgene_diseas_hgmdgene_id_hgmdphenotyp_ac190dbb_uniq; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY diseases_hgmdgene_diseases
    ADD CONSTRAINT diseases_hgmdgene_diseas_hgmdgene_id_hgmdphenotyp_ac190dbb_uniq UNIQUE (hgmdgene_id, hgmdphenotype_id);


--
-- Name: diseases_hgmdgene_diseases diseases_hgmdgene_diseases_pkey; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY diseases_hgmdgene_diseases
    ADD CONSTRAINT diseases_hgmdgene_diseases_pkey PRIMARY KEY (id);


--
-- Name: diseases_hgmdgene diseases_hgmdgene_pkey; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY diseases_hgmdgene
    ADD CONSTRAINT diseases_hgmdgene_pkey PRIMARY KEY (id);


--
-- Name: diseases_hgmdmutation diseases_hgmdmutation_pkey; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY diseases_hgmdmutation
    ADD CONSTRAINT diseases_hgmdmutation_pkey PRIMARY KEY (id);


--
-- Name: diseases_hgmdphenotype diseases_hgmdphenotype_pkey; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY diseases_hgmdphenotype
    ADD CONSTRAINT diseases_hgmdphenotype_pkey PRIMARY KEY (id);


--
-- Name: django_admin_log django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- Name: django_content_type django_content_type_app_label_model_76bd3d3b_uniq; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY django_content_type
    ADD CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq UNIQUE (app_label, model);


--
-- Name: django_content_type django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- Name: django_migrations django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- Name: django_session django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- Name: django_site django_site_domain_a2e37b91_uniq; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY django_site
    ADD CONSTRAINT django_site_domain_a2e37b91_uniq UNIQUE (domain);


--
-- Name: django_site django_site_pkey; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY django_site
    ADD CONSTRAINT django_site_pkey PRIMARY KEY (id);


--
-- Name: djcelery_crontabschedule djcelery_crontabschedule_pkey; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY djcelery_crontabschedule
    ADD CONSTRAINT djcelery_crontabschedule_pkey PRIMARY KEY (id);


--
-- Name: djcelery_intervalschedule djcelery_intervalschedule_pkey; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY djcelery_intervalschedule
    ADD CONSTRAINT djcelery_intervalschedule_pkey PRIMARY KEY (id);


--
-- Name: djcelery_periodictask djcelery_periodictask_name_key; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY djcelery_periodictask
    ADD CONSTRAINT djcelery_periodictask_name_key UNIQUE (name);


--
-- Name: djcelery_periodictask djcelery_periodictask_pkey; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY djcelery_periodictask
    ADD CONSTRAINT djcelery_periodictask_pkey PRIMARY KEY (id);


--
-- Name: djcelery_periodictasks djcelery_periodictasks_pkey; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY djcelery_periodictasks
    ADD CONSTRAINT djcelery_periodictasks_pkey PRIMARY KEY (ident);


--
-- Name: djcelery_taskstate djcelery_taskstate_pkey; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY djcelery_taskstate
    ADD CONSTRAINT djcelery_taskstate_pkey PRIMARY KEY (id);


--
-- Name: djcelery_taskstate djcelery_taskstate_task_id_key; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY djcelery_taskstate
    ADD CONSTRAINT djcelery_taskstate_task_id_key UNIQUE (task_id);


--
-- Name: djcelery_workerstate djcelery_workerstate_hostname_key; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY djcelery_workerstate
    ADD CONSTRAINT djcelery_workerstate_hostname_key UNIQUE (hostname);


--
-- Name: djcelery_workerstate djcelery_workerstate_pkey; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY djcelery_workerstate
    ADD CONSTRAINT djcelery_workerstate_pkey PRIMARY KEY (id);


--
-- Name: djkombu_message djkombu_message_pkey; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY djkombu_message
    ADD CONSTRAINT djkombu_message_pkey PRIMARY KEY (id);


--
-- Name: djkombu_queue djkombu_queue_name_key; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY djkombu_queue
    ADD CONSTRAINT djkombu_queue_name_key UNIQUE (name);


--
-- Name: djkombu_queue djkombu_queue_pkey; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY djkombu_queue
    ADD CONSTRAINT djkombu_queue_pkey PRIMARY KEY (id);


--
-- Name: files_file files_file_pkey; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY files_file
    ADD CONSTRAINT files_file_pkey PRIMARY KEY (id);


--
-- Name: files_s3credential files_s3credential_pkey; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY files_s3credential
    ADD CONSTRAINT files_s3credential_pkey PRIMARY KEY (id);


--
-- Name: genes_cgdcondition genes_cgdcondition_pkey; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY genes_cgdcondition
    ADD CONSTRAINT genes_cgdcondition_pkey PRIMARY KEY (id);


--
-- Name: genes_cgdentry_CONDITIONS genes_cgdentry_CONDITIONS_pkey; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY "genes_cgdentry_CONDITIONS"
    ADD CONSTRAINT "genes_cgdentry_CONDITIONS_pkey" PRIMARY KEY (id);


--
-- Name: genes_cgdentry_CONDITIONS genes_cgdentry_CONDITION_cgdentry_id_cgdcondition_0cababbd_uniq; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY "genes_cgdentry_CONDITIONS"
    ADD CONSTRAINT "genes_cgdentry_CONDITION_cgdentry_id_cgdcondition_0cababbd_uniq" UNIQUE (cgdentry_id, cgdcondition_id);


--
-- Name: genes_cgdentry_INTERVENTION_CATEGORIES genes_cgdentry_INTERVENTION_CATEGORIES_pkey; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY "genes_cgdentry_INTERVENTION_CATEGORIES"
    ADD CONSTRAINT "genes_cgdentry_INTERVENTION_CATEGORIES_pkey" PRIMARY KEY (id);


--
-- Name: genes_cgdentry_INTERVENTION_CATEGORIES genes_cgdentry_INTERVENT_cgdentry_id_intervention_d84d3067_uniq; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY "genes_cgdentry_INTERVENTION_CATEGORIES"
    ADD CONSTRAINT "genes_cgdentry_INTERVENT_cgdentry_id_intervention_d84d3067_uniq" UNIQUE (cgdentry_id, intervention_id);


--
-- Name: genes_cgdentry_MANIFESTATION_CATEGORIES genes_cgdentry_MANIFESTATION_CATEGORIES_pkey; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY "genes_cgdentry_MANIFESTATION_CATEGORIES"
    ADD CONSTRAINT "genes_cgdentry_MANIFESTATION_CATEGORIES_pkey" PRIMARY KEY (id);


--
-- Name: genes_cgdentry_MANIFESTATION_CATEGORIES genes_cgdentry_MANIFESTA_cgdentry_id_manifestatio_97cd96a1_uniq; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY "genes_cgdentry_MANIFESTATION_CATEGORIES"
    ADD CONSTRAINT "genes_cgdentry_MANIFESTA_cgdentry_id_manifestatio_97cd96a1_uniq" UNIQUE (cgdentry_id, manifestation_id);


--
-- Name: genes_cgdentry genes_cgdentry_pkey; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY genes_cgdentry
    ADD CONSTRAINT genes_cgdentry_pkey PRIMARY KEY (id);


--
-- Name: genes_gene_diseases genes_gene_diseases_gene_id_disease_id_11b02615_uniq; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY genes_gene_diseases
    ADD CONSTRAINT genes_gene_diseases_gene_id_disease_id_11b02615_uniq UNIQUE (gene_id, disease_id);


--
-- Name: genes_gene_diseases genes_gene_diseases_pkey; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY genes_gene_diseases
    ADD CONSTRAINT genes_gene_diseases_pkey PRIMARY KEY (id);


--
-- Name: genes_gene genes_gene_pkey; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY genes_gene
    ADD CONSTRAINT genes_gene_pkey PRIMARY KEY (id);


--
-- Name: genes_genecategory_genes genes_genecategory_genes_genecategory_id_gene_id_c8424ff1_uniq; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY genes_genecategory_genes
    ADD CONSTRAINT genes_genecategory_genes_genecategory_id_gene_id_c8424ff1_uniq UNIQUE (genecategory_id, gene_id);


--
-- Name: genes_genecategory_genes genes_genecategory_genes_pkey; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY genes_genecategory_genes
    ADD CONSTRAINT genes_genecategory_genes_pkey PRIMARY KEY (id);


--
-- Name: genes_genecategory genes_genecategory_pkey; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY genes_genecategory
    ADD CONSTRAINT genes_genecategory_pkey PRIMARY KEY (id);


--
-- Name: genes_genegroup genes_genegroup_pkey; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY genes_genegroup
    ADD CONSTRAINT genes_genegroup_pkey PRIMARY KEY (id);


--
-- Name: genes_genelist genes_genelist_pkey; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY genes_genelist
    ADD CONSTRAINT genes_genelist_pkey PRIMARY KEY (id);


--
-- Name: genes_goterm_children genes_goterm_children_from_goterm_id_to_goterm_id_3a8879ea_uniq; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY genes_goterm_children
    ADD CONSTRAINT genes_goterm_children_from_goterm_id_to_goterm_id_3a8879ea_uniq UNIQUE (from_goterm_id, to_goterm_id);


--
-- Name: genes_goterm_children genes_goterm_children_pkey; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY genes_goterm_children
    ADD CONSTRAINT genes_goterm_children_pkey PRIMARY KEY (id);


--
-- Name: genes_goterm_parents genes_goterm_parents_from_goterm_id_to_goterm_id_16188c33_uniq; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY genes_goterm_parents
    ADD CONSTRAINT genes_goterm_parents_from_goterm_id_to_goterm_id_16188c33_uniq UNIQUE (from_goterm_id, to_goterm_id);


--
-- Name: genes_goterm_parents genes_goterm_parents_pkey; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY genes_goterm_parents
    ADD CONSTRAINT genes_goterm_parents_pkey PRIMARY KEY (id);


--
-- Name: genes_goterm genes_goterm_pkey; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY genes_goterm
    ADD CONSTRAINT genes_goterm_pkey PRIMARY KEY (id);


--
-- Name: genes_intervention genes_intervention_pkey; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY genes_intervention
    ADD CONSTRAINT genes_intervention_pkey PRIMARY KEY (id);


--
-- Name: genes_manifestation genes_manifestation_pkey; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY genes_manifestation
    ADD CONSTRAINT genes_manifestation_pkey PRIMARY KEY (id);


--
-- Name: genes_membership genes_membership_pkey; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY genes_membership
    ADD CONSTRAINT genes_membership_pkey PRIMARY KEY (id);


--
-- Name: individuals_controlgroup individuals_controlgroup_pkey; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY individuals_controlgroup
    ADD CONSTRAINT individuals_controlgroup_pkey PRIMARY KEY (id);


--
-- Name: individuals_controlvariant individuals_controlvariant_pkey; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY individuals_controlvariant
    ADD CONSTRAINT individuals_controlvariant_pkey PRIMARY KEY (id);


--
-- Name: individuals_group_members individuals_group_members_group_id_individual_id_997e094b_uniq; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY individuals_group_members
    ADD CONSTRAINT individuals_group_members_group_id_individual_id_997e094b_uniq UNIQUE (group_id, individual_id);


--
-- Name: individuals_group_members individuals_group_members_pkey; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY individuals_group_members
    ADD CONSTRAINT individuals_group_members_pkey PRIMARY KEY (id);


--
-- Name: individuals_group individuals_group_pkey; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY individuals_group
    ADD CONSTRAINT individuals_group_pkey PRIMARY KEY (id);


--
-- Name: individuals_individual individuals_individual_pkey; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY individuals_individual
    ADD CONSTRAINT individuals_individual_pkey PRIMARY KEY (id);


--
-- Name: individuals_individual_shared_with_users individuals_individual_s_individual_id_user_id_35f5fae4_uniq; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY individuals_individual_shared_with_users
    ADD CONSTRAINT individuals_individual_s_individual_id_user_id_35f5fae4_uniq UNIQUE (individual_id, user_id);


--
-- Name: individuals_individual_shared_with_groups individuals_individual_s_individual_id_usergroup__7984bff9_uniq; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY individuals_individual_shared_with_groups
    ADD CONSTRAINT individuals_individual_s_individual_id_usergroup__7984bff9_uniq UNIQUE (individual_id, usergroup_id);


--
-- Name: individuals_individual_shared_with_groups individuals_individual_shared_with_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY individuals_individual_shared_with_groups
    ADD CONSTRAINT individuals_individual_shared_with_groups_pkey PRIMARY KEY (id);


--
-- Name: individuals_individual_shared_with_users individuals_individual_shared_with_users_pkey; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY individuals_individual_shared_with_users
    ADD CONSTRAINT individuals_individual_shared_with_users_pkey PRIMARY KEY (id);


--
-- Name: individuals_usergroup_members individuals_usergroup_me_usergroup_id_user_id_c4e9e2be_uniq; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY individuals_usergroup_members
    ADD CONSTRAINT individuals_usergroup_me_usergroup_id_user_id_c4e9e2be_uniq UNIQUE (usergroup_id, user_id);


--
-- Name: individuals_usergroup_members individuals_usergroup_members_pkey; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY individuals_usergroup_members
    ADD CONSTRAINT individuals_usergroup_members_pkey PRIMARY KEY (id);


--
-- Name: individuals_usergroup individuals_usergroup_pkey; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY individuals_usergroup
    ADD CONSTRAINT individuals_usergroup_pkey PRIMARY KEY (id);


--
-- Name: projects_project_files projects_project_files_pkey; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY projects_project_files
    ADD CONSTRAINT projects_project_files_pkey PRIMARY KEY (id);


--
-- Name: projects_project_files projects_project_files_project_id_file_id_40071e86_uniq; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY projects_project_files
    ADD CONSTRAINT projects_project_files_project_id_file_id_40071e86_uniq UNIQUE (project_id, file_id);


--
-- Name: projects_project_groups projects_project_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY projects_project_groups
    ADD CONSTRAINT projects_project_groups_pkey PRIMARY KEY (id);


--
-- Name: projects_project_groups projects_project_groups_project_id_group_id_036267ce_uniq; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY projects_project_groups
    ADD CONSTRAINT projects_project_groups_project_id_group_id_036267ce_uniq UNIQUE (project_id, group_id);


--
-- Name: projects_project_individuals projects_project_individ_project_id_individual_id_36f81ade_uniq; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY projects_project_individuals
    ADD CONSTRAINT projects_project_individ_project_id_individual_id_36f81ade_uniq UNIQUE (project_id, individual_id);


--
-- Name: projects_project_individuals projects_project_individuals_pkey; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY projects_project_individuals
    ADD CONSTRAINT projects_project_individuals_pkey PRIMARY KEY (id);


--
-- Name: projects_project_members projects_project_members_pkey; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY projects_project_members
    ADD CONSTRAINT projects_project_members_pkey PRIMARY KEY (id);


--
-- Name: projects_project_members projects_project_members_project_id_user_id_d03019c7_uniq; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY projects_project_members
    ADD CONSTRAINT projects_project_members_project_id_user_id_d03019c7_uniq UNIQUE (project_id, user_id);


--
-- Name: projects_project projects_project_pkey; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY projects_project
    ADD CONSTRAINT projects_project_pkey PRIMARY KEY (id);


--
-- Name: socialaccount_socialaccount socialaccount_socialaccount_pkey; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY socialaccount_socialaccount
    ADD CONSTRAINT socialaccount_socialaccount_pkey PRIMARY KEY (id);


--
-- Name: socialaccount_socialaccount socialaccount_socialaccount_provider_uid_fc810c6e_uniq; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY socialaccount_socialaccount
    ADD CONSTRAINT socialaccount_socialaccount_provider_uid_fc810c6e_uniq UNIQUE (provider, uid);


--
-- Name: socialaccount_socialapp_sites socialaccount_socialapp__socialapp_id_site_id_71a9a768_uniq; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY socialaccount_socialapp_sites
    ADD CONSTRAINT socialaccount_socialapp__socialapp_id_site_id_71a9a768_uniq UNIQUE (socialapp_id, site_id);


--
-- Name: socialaccount_socialapp socialaccount_socialapp_pkey; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY socialaccount_socialapp
    ADD CONSTRAINT socialaccount_socialapp_pkey PRIMARY KEY (id);


--
-- Name: socialaccount_socialapp_sites socialaccount_socialapp_sites_pkey; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY socialaccount_socialapp_sites
    ADD CONSTRAINT socialaccount_socialapp_sites_pkey PRIMARY KEY (id);


--
-- Name: socialaccount_socialtoken socialaccount_socialtoken_app_id_account_id_fca4e0ac_uniq; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY socialaccount_socialtoken
    ADD CONSTRAINT socialaccount_socialtoken_app_id_account_id_fca4e0ac_uniq UNIQUE (app_id, account_id);


--
-- Name: socialaccount_socialtoken socialaccount_socialtoken_pkey; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY socialaccount_socialtoken
    ADD CONSTRAINT socialaccount_socialtoken_pkey PRIMARY KEY (id);


--
-- Name: variants_variant variants_variant_pkey; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY variants_variant
    ADD CONSTRAINT variants_variant_pkey PRIMARY KEY (id);


--
-- Name: variants_variantannotation variants_variantannotation_pkey; Type: CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY variants_variantannotation
    ADD CONSTRAINT variants_variantannotation_pkey PRIMARY KEY (id);


--
-- Name: account_emailaddress_email_03be32b2_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX account_emailaddress_email_03be32b2_like ON account_emailaddress USING btree (email varchar_pattern_ops);


--
-- Name: account_emailaddress_user_id_2c513194; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX account_emailaddress_user_id_2c513194 ON account_emailaddress USING btree (user_id);


--
-- Name: account_emailconfirmation_email_address_id_5b7f8c58; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX account_emailconfirmation_email_address_id_5b7f8c58 ON account_emailconfirmation USING btree (email_address_id);


--
-- Name: account_emailconfirmation_key_f43612bd_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX account_emailconfirmation_key_f43612bd_like ON account_emailconfirmation USING btree (key varchar_pattern_ops);


--
-- Name: auth_group_name_a6ea08ec_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX auth_group_name_a6ea08ec_like ON auth_group USING btree (name varchar_pattern_ops);


--
-- Name: auth_group_permissions_group_id_b120cbf9; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX auth_group_permissions_group_id_b120cbf9 ON auth_group_permissions USING btree (group_id);


--
-- Name: auth_group_permissions_permission_id_84c5c92e; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX auth_group_permissions_permission_id_84c5c92e ON auth_group_permissions USING btree (permission_id);


--
-- Name: auth_permission_content_type_id_2f476e4b; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX auth_permission_content_type_id_2f476e4b ON auth_permission USING btree (content_type_id);


--
-- Name: auth_user_groups_group_id_97559544; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX auth_user_groups_group_id_97559544 ON auth_user_groups USING btree (group_id);


--
-- Name: auth_user_groups_user_id_6a12ed8b; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX auth_user_groups_user_id_6a12ed8b ON auth_user_groups USING btree (user_id);


--
-- Name: auth_user_user_permissions_permission_id_1fbb5f2c; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX auth_user_user_permissions_permission_id_1fbb5f2c ON auth_user_user_permissions USING btree (permission_id);


--
-- Name: auth_user_user_permissions_user_id_a95ead1b; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX auth_user_user_permissions_user_id_a95ead1b ON auth_user_user_permissions USING btree (user_id);


--
-- Name: auth_user_username_6821ab7c_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX auth_user_username_6821ab7c_like ON auth_user USING btree (username varchar_pattern_ops);


--
-- Name: cases_case_case_groups_case_id_2c56addb; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX cases_case_case_groups_case_id_2c56addb ON cases_case_case_groups USING btree (case_id);


--
-- Name: cases_case_case_groups_group_id_2d600616; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX cases_case_case_groups_group_id_2d600616 ON cases_case_case_groups USING btree (group_id);


--
-- Name: cases_case_cases_case_id_90e8cfc0; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX cases_case_cases_case_id_90e8cfc0 ON cases_case_cases USING btree (case_id);


--
-- Name: cases_case_cases_individual_id_359c652b; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX cases_case_cases_individual_id_359c652b ON cases_case_cases USING btree (individual_id);


--
-- Name: cases_case_children_case_id_c6e7d0f9; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX cases_case_children_case_id_c6e7d0f9 ON cases_case_children USING btree (case_id);


--
-- Name: cases_case_children_individual_id_548cbcd1; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX cases_case_children_individual_id_548cbcd1 ON cases_case_children USING btree (individual_id);


--
-- Name: cases_case_control_groups_case_id_a1d0d7d0; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX cases_case_control_groups_case_id_a1d0d7d0 ON cases_case_control_groups USING btree (case_id);


--
-- Name: cases_case_control_groups_group_id_6c361188; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX cases_case_control_groups_group_id_6c361188 ON cases_case_control_groups USING btree (group_id);


--
-- Name: cases_case_controls_case_id_ce379262; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX cases_case_controls_case_id_ce379262 ON cases_case_controls USING btree (case_id);


--
-- Name: cases_case_controls_individual_id_b3771c33; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX cases_case_controls_individual_id_b3771c33 ON cases_case_controls USING btree (individual_id);


--
-- Name: cases_case_father_id_d3aa9ff7; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX cases_case_father_id_d3aa9ff7 ON cases_case USING btree (father_id);


--
-- Name: cases_case_mother_id_60214b94; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX cases_case_mother_id_60214b94 ON cases_case USING btree (mother_id);


--
-- Name: cases_case_shared_with_groups_case_id_b4d253d9; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX cases_case_shared_with_groups_case_id_b4d253d9 ON cases_case_shared_with_groups USING btree (case_id);


--
-- Name: cases_case_shared_with_groups_group_id_eff5b712; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX cases_case_shared_with_groups_group_id_eff5b712 ON cases_case_shared_with_groups USING btree (group_id);


--
-- Name: cases_case_shared_with_users_case_id_c4a1f778; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX cases_case_shared_with_users_case_id_c4a1f778 ON cases_case_shared_with_users USING btree (case_id);


--
-- Name: cases_case_shared_with_users_user_id_291730e1; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX cases_case_shared_with_users_user_id_291730e1 ON cases_case_shared_with_users USING btree (user_id);


--
-- Name: cases_case_user_id_bc4e6df6; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX cases_case_user_id_bc4e6df6 ON cases_case USING btree (user_id);


--
-- Name: celery_taskmeta_hidden_23fd02dc; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX celery_taskmeta_hidden_23fd02dc ON celery_taskmeta USING btree (hidden);


--
-- Name: celery_taskmeta_task_id_9558b198_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX celery_taskmeta_task_id_9558b198_like ON celery_taskmeta USING btree (task_id varchar_pattern_ops);


--
-- Name: celery_tasksetmeta_hidden_593cfc24; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX celery_tasksetmeta_hidden_593cfc24 ON celery_tasksetmeta USING btree (hidden);


--
-- Name: celery_tasksetmeta_taskset_id_a5a1d4ae_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX celery_tasksetmeta_taskset_id_a5a1d4ae_like ON celery_tasksetmeta USING btree (taskset_id varchar_pattern_ops);


--
-- Name: diseases_gene_diseases_disease_id_bd05da51; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX diseases_gene_diseases_disease_id_bd05da51 ON diseases_gene_diseases USING btree (disease_id);


--
-- Name: diseases_gene_diseases_gene_id_9b15fab6; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX diseases_gene_diseases_gene_id_9b15fab6 ON diseases_gene_diseases USING btree (gene_id);


--
-- Name: diseases_hgmdgene_diseases_hgmdgene_id_d9f66777; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX diseases_hgmdgene_diseases_hgmdgene_id_d9f66777 ON diseases_hgmdgene_diseases USING btree (hgmdgene_id);


--
-- Name: diseases_hgmdgene_diseases_hgmdphenotype_id_c4b4eb3f; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX diseases_hgmdgene_diseases_hgmdphenotype_id_c4b4eb3f ON diseases_hgmdgene_diseases USING btree (hgmdphenotype_id);


--
-- Name: diseases_hgmdmutation_gene_id_4286e0ed; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX diseases_hgmdmutation_gene_id_4286e0ed ON diseases_hgmdmutation USING btree (gene_id);


--
-- Name: diseases_hgmdmutation_phenotype_id_5343ded5; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX diseases_hgmdmutation_phenotype_id_5343ded5 ON diseases_hgmdmutation USING btree (phenotype_id);


--
-- Name: django_admin_log_content_type_id_c4bce8eb; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX django_admin_log_content_type_id_c4bce8eb ON django_admin_log USING btree (content_type_id);


--
-- Name: django_admin_log_user_id_c564eba6; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX django_admin_log_user_id_c564eba6 ON django_admin_log USING btree (user_id);


--
-- Name: django_session_expire_date_a5c62663; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX django_session_expire_date_a5c62663 ON django_session USING btree (expire_date);


--
-- Name: django_session_session_key_c0390e0f_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX django_session_session_key_c0390e0f_like ON django_session USING btree (session_key varchar_pattern_ops);


--
-- Name: django_site_domain_a2e37b91_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX django_site_domain_a2e37b91_like ON django_site USING btree (domain varchar_pattern_ops);


--
-- Name: djcelery_periodictask_crontab_id_75609bab; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX djcelery_periodictask_crontab_id_75609bab ON djcelery_periodictask USING btree (crontab_id);


--
-- Name: djcelery_periodictask_interval_id_b426ab02; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX djcelery_periodictask_interval_id_b426ab02 ON djcelery_periodictask USING btree (interval_id);


--
-- Name: djcelery_periodictask_name_cb62cda9_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX djcelery_periodictask_name_cb62cda9_like ON djcelery_periodictask USING btree (name varchar_pattern_ops);


--
-- Name: djcelery_taskstate_hidden_c3905e57; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX djcelery_taskstate_hidden_c3905e57 ON djcelery_taskstate USING btree (hidden);


--
-- Name: djcelery_taskstate_name_8af9eded; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX djcelery_taskstate_name_8af9eded ON djcelery_taskstate USING btree (name);


--
-- Name: djcelery_taskstate_name_8af9eded_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX djcelery_taskstate_name_8af9eded_like ON djcelery_taskstate USING btree (name varchar_pattern_ops);


--
-- Name: djcelery_taskstate_state_53543be4; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX djcelery_taskstate_state_53543be4 ON djcelery_taskstate USING btree (state);


--
-- Name: djcelery_taskstate_state_53543be4_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX djcelery_taskstate_state_53543be4_like ON djcelery_taskstate USING btree (state varchar_pattern_ops);


--
-- Name: djcelery_taskstate_task_id_9d2efdb5_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX djcelery_taskstate_task_id_9d2efdb5_like ON djcelery_taskstate USING btree (task_id varchar_pattern_ops);


--
-- Name: djcelery_taskstate_tstamp_4c3f93a1; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX djcelery_taskstate_tstamp_4c3f93a1 ON djcelery_taskstate USING btree (tstamp);


--
-- Name: djcelery_taskstate_worker_id_f7f57a05; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX djcelery_taskstate_worker_id_f7f57a05 ON djcelery_taskstate USING btree (worker_id);


--
-- Name: djcelery_workerstate_hostname_b31c7fab_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX djcelery_workerstate_hostname_b31c7fab_like ON djcelery_workerstate USING btree (hostname varchar_pattern_ops);


--
-- Name: djcelery_workerstate_last_heartbeat_4539b544; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX djcelery_workerstate_last_heartbeat_4539b544 ON djcelery_workerstate USING btree (last_heartbeat);


--
-- Name: djkombu_message_queue_id_38d205a7; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX djkombu_message_queue_id_38d205a7 ON djkombu_message USING btree (queue_id);


--
-- Name: djkombu_message_sent_at_680ecd55; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX djkombu_message_sent_at_680ecd55 ON djkombu_message USING btree (sent_at);


--
-- Name: djkombu_message_visible_3ca5f33e; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX djkombu_message_visible_3ca5f33e ON djkombu_message USING btree (visible);


--
-- Name: djkombu_queue_name_8b43c728_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX djkombu_queue_name_8b43c728_like ON djkombu_queue USING btree (name varchar_pattern_ops);


--
-- Name: genes_cgdentry_CONDITIONS_cgdcondition_id_953c0630; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "genes_cgdentry_CONDITIONS_cgdcondition_id_953c0630" ON "genes_cgdentry_CONDITIONS" USING btree (cgdcondition_id);


--
-- Name: genes_cgdentry_CONDITIONS_cgdentry_id_7c9ad17c; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "genes_cgdentry_CONDITIONS_cgdentry_id_7c9ad17c" ON "genes_cgdentry_CONDITIONS" USING btree (cgdentry_id);


--
-- Name: genes_cgdentry_INTERVENTION_CATEGORIES_cgdentry_id_2660621e; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "genes_cgdentry_INTERVENTION_CATEGORIES_cgdentry_id_2660621e" ON "genes_cgdentry_INTERVENTION_CATEGORIES" USING btree (cgdentry_id);


--
-- Name: genes_cgdentry_INTERVENTION_CATEGORIES_intervention_id_09582a0c; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "genes_cgdentry_INTERVENTION_CATEGORIES_intervention_id_09582a0c" ON "genes_cgdentry_INTERVENTION_CATEGORIES" USING btree (intervention_id);


--
-- Name: genes_cgdentry_MANIFESTATION_CATEGORIES_cgdentry_id_fec24495; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "genes_cgdentry_MANIFESTATION_CATEGORIES_cgdentry_id_fec24495" ON "genes_cgdentry_MANIFESTATION_CATEGORIES" USING btree (cgdentry_id);


--
-- Name: genes_cgdentry_MANIFESTATI_manifestation_id_04303717; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "genes_cgdentry_MANIFESTATI_manifestation_id_04303717" ON "genes_cgdentry_MANIFESTATION_CATEGORIES" USING btree (manifestation_id);


--
-- Name: genes_gene_diseases_disease_id_58690f60; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX genes_gene_diseases_disease_id_58690f60 ON genes_gene_diseases USING btree (disease_id);


--
-- Name: genes_gene_diseases_gene_id_4ff7115e; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX genes_gene_diseases_gene_id_4ff7115e ON genes_gene_diseases USING btree (gene_id);


--
-- Name: genes_genecategory_genes_gene_id_bdfa6678; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX genes_genecategory_genes_gene_id_bdfa6678 ON genes_genecategory_genes USING btree (gene_id);


--
-- Name: genes_genecategory_genes_genecategory_id_b0c0cabd; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX genes_genecategory_genes_genecategory_id_b0c0cabd ON genes_genecategory_genes USING btree (genecategory_id);


--
-- Name: genes_genelist_user_id_eb300f6d; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX genes_genelist_user_id_eb300f6d ON genes_genelist USING btree (user_id);


--
-- Name: genes_goterm_children_from_goterm_id_98c9c1f0; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX genes_goterm_children_from_goterm_id_98c9c1f0 ON genes_goterm_children USING btree (from_goterm_id);


--
-- Name: genes_goterm_children_to_goterm_id_43061461; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX genes_goterm_children_to_goterm_id_43061461 ON genes_goterm_children USING btree (to_goterm_id);


--
-- Name: genes_goterm_parents_from_goterm_id_164ed754; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX genes_goterm_parents_from_goterm_id_164ed754 ON genes_goterm_parents USING btree (from_goterm_id);


--
-- Name: genes_goterm_parents_to_goterm_id_d1ec2c5d; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX genes_goterm_parents_to_goterm_id_d1ec2c5d ON genes_goterm_parents USING btree (to_goterm_id);


--
-- Name: genes_membership_gene_id_83331c66; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX genes_membership_gene_id_83331c66 ON genes_membership USING btree (gene_id);


--
-- Name: genes_membership_group_id_f4b3d9ed; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX genes_membership_group_id_f4b3d9ed ON genes_membership USING btree (group_id);


--
-- Name: individuals_controlvariant_controlgroup_id_6b62649d; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX individuals_controlvariant_controlgroup_id_6b62649d ON individuals_controlvariant USING btree (controlgroup_id);


--
-- Name: individuals_controlvariant_index_8afcfc4a; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX individuals_controlvariant_index_8afcfc4a ON individuals_controlvariant USING btree (index);


--
-- Name: individuals_controlvariant_index_8afcfc4a_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX individuals_controlvariant_index_8afcfc4a_like ON individuals_controlvariant USING btree (index text_pattern_ops);


--
-- Name: individuals_group_members_group_id_ea56f429; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX individuals_group_members_group_id_ea56f429 ON individuals_group_members USING btree (group_id);


--
-- Name: individuals_group_members_individual_id_497e1be9; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX individuals_group_members_individual_id_497e1be9 ON individuals_group_members USING btree (individual_id);


--
-- Name: individuals_individual_sha_individual_id_05de08af; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX individuals_individual_sha_individual_id_05de08af ON individuals_individual_shared_with_groups USING btree (individual_id);


--
-- Name: individuals_individual_shared_with_groups_usergroup_id_e13d283c; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX individuals_individual_shared_with_groups_usergroup_id_e13d283c ON individuals_individual_shared_with_groups USING btree (usergroup_id);


--
-- Name: individuals_individual_shared_with_users_individual_id_47081c26; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX individuals_individual_shared_with_users_individual_id_47081c26 ON individuals_individual_shared_with_users USING btree (individual_id);


--
-- Name: individuals_individual_shared_with_users_user_id_b9f3fea8; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX individuals_individual_shared_with_users_user_id_b9f3fea8 ON individuals_individual_shared_with_users USING btree (user_id);


--
-- Name: individuals_individual_user_id_8e362273; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX individuals_individual_user_id_8e362273 ON individuals_individual USING btree (user_id);


--
-- Name: individuals_usergroup_members_user_id_92da6911; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX individuals_usergroup_members_user_id_92da6911 ON individuals_usergroup_members USING btree (user_id);


--
-- Name: individuals_usergroup_members_usergroup_id_88110220; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX individuals_usergroup_members_usergroup_id_88110220 ON individuals_usergroup_members USING btree (usergroup_id);


--
-- Name: projects_project_files_file_id_d1fa60e4; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX projects_project_files_file_id_d1fa60e4 ON projects_project_files USING btree (file_id);


--
-- Name: projects_project_files_project_id_1b037a58; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX projects_project_files_project_id_1b037a58 ON projects_project_files USING btree (project_id);


--
-- Name: projects_project_groups_group_id_90ac8d97; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX projects_project_groups_group_id_90ac8d97 ON projects_project_groups USING btree (group_id);


--
-- Name: projects_project_groups_project_id_3bf040aa; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX projects_project_groups_project_id_3bf040aa ON projects_project_groups USING btree (project_id);


--
-- Name: projects_project_individuals_individual_id_5ca3bf25; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX projects_project_individuals_individual_id_5ca3bf25 ON projects_project_individuals USING btree (individual_id);


--
-- Name: projects_project_individuals_project_id_b9258353; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX projects_project_individuals_project_id_b9258353 ON projects_project_individuals USING btree (project_id);


--
-- Name: projects_project_members_project_id_6a04b77b; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX projects_project_members_project_id_6a04b77b ON projects_project_members USING btree (project_id);


--
-- Name: projects_project_members_user_id_f7cc124d; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX projects_project_members_user_id_f7cc124d ON projects_project_members USING btree (user_id);


--
-- Name: projects_project_user_id_719f19dd; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX projects_project_user_id_719f19dd ON projects_project USING btree (user_id);


--
-- Name: socialaccount_socialaccount_user_id_8146e70c; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX socialaccount_socialaccount_user_id_8146e70c ON socialaccount_socialaccount USING btree (user_id);


--
-- Name: socialaccount_socialapp_sites_site_id_2579dee5; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX socialaccount_socialapp_sites_site_id_2579dee5 ON socialaccount_socialapp_sites USING btree (site_id);


--
-- Name: socialaccount_socialapp_sites_socialapp_id_97fb6e7d; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX socialaccount_socialapp_sites_socialapp_id_97fb6e7d ON socialaccount_socialapp_sites USING btree (socialapp_id);


--
-- Name: socialaccount_socialtoken_account_id_951f210e; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX socialaccount_socialtoken_account_id_951f210e ON socialaccount_socialtoken USING btree (account_id);


--
-- Name: socialaccount_socialtoken_app_id_636a42d7; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX socialaccount_socialtoken_app_id_636a42d7 ON socialaccount_socialtoken USING btree (app_id);


--
-- Name: variants_variant_chr_6b01b007; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variant_chr_6b01b007 ON variants_variant USING btree (chr);


--
-- Name: variants_variant_chr_6b01b007_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variant_chr_6b01b007_like ON variants_variant USING btree (chr varchar_pattern_ops);


--
-- Name: variants_variant_index_5e0eba2e; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variant_index_5e0eba2e ON variants_variant USING btree (index);


--
-- Name: variants_variant_index_5e0eba2e_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variant_index_5e0eba2e_like ON variants_variant USING btree (index text_pattern_ops);


--
-- Name: variants_variant_pos_2805f798; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variant_pos_2805f798 ON variants_variant USING btree (pos);


--
-- Name: variants_variantannotati_FATHMM_converted_ranksco_8e20e21a_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotati_FATHMM_converted_ranksco_8e20e21a_like" ON variants_variantannotation USING btree ("FATHMM_converted_rankscore" text_pattern_ops);


--
-- Name: variants_variantannotati_GM12878_confidence_value_b95f3451_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotati_GM12878_confidence_value_b95f3451_like" ON variants_variantannotation USING btree ("GM12878_confidence_value" text_pattern_ops);


--
-- Name: variants_variantannotati_GM12878_fitCons_rankscor_c2f322c1_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotati_GM12878_fitCons_rankscor_c2f322c1_like" ON variants_variantannotation USING btree ("GM12878_fitCons_rankscore" text_pattern_ops);


--
-- Name: variants_variantannotati_GenoCanyon_score_ranksco_f58d27db_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotati_GenoCanyon_score_ranksco_f58d27db_like" ON variants_variantannotation USING btree ("GenoCanyon_score_rankscore" text_pattern_ops);


--
-- Name: variants_variantannotati_H1_hESC_confidence_value_aa804d36_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotati_H1_hESC_confidence_value_aa804d36_like" ON variants_variantannotation USING btree ("H1_hESC_confidence_value" text_pattern_ops);


--
-- Name: variants_variantannotati_H1_hESC_fitCons_rankscor_bfe24fa1_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotati_H1_hESC_fitCons_rankscor_bfe24fa1_like" ON variants_variantannotation USING btree ("H1_hESC_fitCons_rankscore" text_pattern_ops);


--
-- Name: variants_variantannotati_HUVEC_fitCons_rankscore_d5a2ea45_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotati_HUVEC_fitCons_rankscore_d5a2ea45_like" ON variants_variantannotation USING btree ("HUVEC_fitCons_rankscore" text_pattern_ops);


--
-- Name: variants_variantannotati_LRT_converted_rankscore_6893c896_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotati_LRT_converted_rankscore_6893c896_like" ON variants_variantannotation USING btree ("LRT_converted_rankscore" text_pattern_ops);


--
-- Name: variants_variantannotati_MutationAssessor_Uniprot_74522271_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotati_MutationAssessor_Uniprot_74522271_like" ON variants_variantannotation USING btree ("MutationAssessor_UniprotID" text_pattern_ops);


--
-- Name: variants_variantannotati_MutationAssessor_ranksco_49a0066f_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotati_MutationAssessor_ranksco_49a0066f_like" ON variants_variantannotation USING btree ("MutationAssessor_rankscore" text_pattern_ops);


--
-- Name: variants_variantannotati_MutationAssessor_variant_1d33911f_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotati_MutationAssessor_variant_1d33911f_like" ON variants_variantannotation USING btree ("MutationAssessor_variant" text_pattern_ops);


--
-- Name: variants_variantannotati_MutationTaster_converted_aecc47ab_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotati_MutationTaster_converted_aecc47ab_like" ON variants_variantannotation USING btree ("MutationTaster_converted_rankscore" text_pattern_ops);


--
-- Name: variants_variantannotati_PROVEAN_converted_ranksc_89206816_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotati_PROVEAN_converted_ranksc_89206816_like" ON variants_variantannotation USING btree ("PROVEAN_converted_rankscore" text_pattern_ops);


--
-- Name: variants_variantannotati_Polyphen2_HDIV_rankscore_fd0fe3e9_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotati_Polyphen2_HDIV_rankscore_fd0fe3e9_like" ON variants_variantannotation USING btree ("Polyphen2_HDIV_rankscore" text_pattern_ops);


--
-- Name: variants_variantannotati_Polyphen2_HVAR_rankscore_d1b0c147_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotati_Polyphen2_HVAR_rankscore_d1b0c147_like" ON variants_variantannotation USING btree ("Polyphen2_HVAR_rankscore" text_pattern_ops);


--
-- Name: variants_variantannotati_SIFT_converted_rankscore_e6284979_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotati_SIFT_converted_rankscore_e6284979_like" ON variants_variantannotation USING btree ("SIFT_converted_rankscore" text_pattern_ops);


--
-- Name: variants_variantannotati_SiPhy_29way_logOdds_rank_17078f4d_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotati_SiPhy_29way_logOdds_rank_17078f4d_like" ON variants_variantannotation USING btree ("SiPhy_29way_logOdds_rankscore" text_pattern_ops);


--
-- Name: variants_variantannotati_Uniprot_aapos_Polyphen2_90ecae1a_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotati_Uniprot_aapos_Polyphen2_90ecae1a_like" ON variants_variantannotation USING btree ("Uniprot_aapos_Polyphen2" text_pattern_ops);


--
-- Name: variants_variantannotati_fathmm_MKL_coding_group_e8ac587b_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotati_fathmm_MKL_coding_group_e8ac587b_like" ON variants_variantannotation USING btree ("fathmm_MKL_coding_group" text_pattern_ops);


--
-- Name: variants_variantannotati_fathmm_MKL_coding_ranksc_7f0a15b6_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotati_fathmm_MKL_coding_ranksc_7f0a15b6_like" ON variants_variantannotation USING btree ("fathmm_MKL_coding_rankscore" text_pattern_ops);


--
-- Name: variants_variantannotati_fathmm_MKL_coding_score_55a6a0ff_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotati_fathmm_MKL_coding_score_55a6a0ff_like" ON variants_variantannotation USING btree ("fathmm_MKL_coding_score" text_pattern_ops);


--
-- Name: variants_variantannotati_integrated_confidence_va_45c8c0b0_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variantannotati_integrated_confidence_va_45c8c0b0_like ON variants_variantannotation USING btree (integrated_confidence_value text_pattern_ops);


--
-- Name: variants_variantannotati_integrated_fitCons_ranks_bd92809e_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotati_integrated_fitCons_ranks_bd92809e_like" ON variants_variantannotation USING btree ("integrated_fitCons_rankscore" text_pattern_ops);


--
-- Name: variants_variantannotati_integrated_fitCons_score_91425982_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotati_integrated_fitCons_score_91425982_like" ON variants_variantannotation USING btree ("integrated_fitCons_score" text_pattern_ops);


--
-- Name: variants_variantannotati_phastCons100way_vertebra_0fc58510_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotati_phastCons100way_vertebra_0fc58510_like" ON variants_variantannotation USING btree ("phastCons100way_vertebrate_rankscore" text_pattern_ops);


--
-- Name: variants_variantannotati_phastCons100way_vertebra_9e2f68b8_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotati_phastCons100way_vertebra_9e2f68b8_like" ON variants_variantannotation USING btree ("phastCons100way_vertebrate" text_pattern_ops);


--
-- Name: variants_variantannotati_phastCons20way_mammalian_b5d6ff44_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotati_phastCons20way_mammalian_b5d6ff44_like" ON variants_variantannotation USING btree ("phastCons20way_mammalian" text_pattern_ops);


--
-- Name: variants_variantannotati_phastCons20way_mammalian_df6cf11f_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotati_phastCons20way_mammalian_df6cf11f_like" ON variants_variantannotation USING btree ("phastCons20way_mammalian_rankscore" text_pattern_ops);


--
-- Name: variants_variantannotati_phyloP100way_vertebrate_8d5ebe4e_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotati_phyloP100way_vertebrate_8d5ebe4e_like" ON variants_variantannotation USING btree ("phyloP100way_vertebrate" text_pattern_ops);


--
-- Name: variants_variantannotati_phyloP100way_vertebrate__962a58b5_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotati_phyloP100way_vertebrate__962a58b5_like" ON variants_variantannotation USING btree ("phyloP100way_vertebrate_rankscore" text_pattern_ops);


--
-- Name: variants_variantannotati_phyloP20way_mammalian_ra_244316c3_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotati_phyloP20way_mammalian_ra_244316c3_like" ON variants_variantannotation USING btree ("phyloP20way_mammalian_rankscore" text_pattern_ops);


--
-- Name: variants_variantannotation_CADD_phred_f56ff8e6; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_CADD_phred_f56ff8e6" ON variants_variantannotation USING btree ("CADD_phred");


--
-- Name: variants_variantannotation_CADD_phred_f56ff8e6_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_CADD_phred_f56ff8e6_like" ON variants_variantannotation USING btree ("CADD_phred" text_pattern_ops);


--
-- Name: variants_variantannotation_CADD_raw_248367dc; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_CADD_raw_248367dc" ON variants_variantannotation USING btree ("CADD_raw");


--
-- Name: variants_variantannotation_CADD_raw_248367dc_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_CADD_raw_248367dc_like" ON variants_variantannotation USING btree ("CADD_raw" text_pattern_ops);


--
-- Name: variants_variantannotation_CADD_raw_rankscore_a99216c5; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_CADD_raw_rankscore_a99216c5" ON variants_variantannotation USING btree ("CADD_raw_rankscore");


--
-- Name: variants_variantannotation_CADD_raw_rankscore_a99216c5_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_CADD_raw_rankscore_a99216c5_like" ON variants_variantannotation USING btree ("CADD_raw_rankscore" text_pattern_ops);


--
-- Name: variants_variantannotation_DANN_rankscore_2f0ca2c2; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_DANN_rankscore_2f0ca2c2" ON variants_variantannotation USING btree ("DANN_rankscore");


--
-- Name: variants_variantannotation_DANN_rankscore_2f0ca2c2_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_DANN_rankscore_2f0ca2c2_like" ON variants_variantannotation USING btree ("DANN_rankscore" text_pattern_ops);


--
-- Name: variants_variantannotation_DANN_score_0cc0efaa; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_DANN_score_0cc0efaa" ON variants_variantannotation USING btree ("DANN_score");


--
-- Name: variants_variantannotation_DANN_score_0cc0efaa_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_DANN_score_0cc0efaa_like" ON variants_variantannotation USING btree ("DANN_score" text_pattern_ops);


--
-- Name: variants_variantannotation_Eigen_PC_raw_272cd301; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_Eigen_PC_raw_272cd301" ON variants_variantannotation USING btree ("Eigen_PC_raw");


--
-- Name: variants_variantannotation_Eigen_PC_raw_272cd301_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_Eigen_PC_raw_272cd301_like" ON variants_variantannotation USING btree ("Eigen_PC_raw" text_pattern_ops);


--
-- Name: variants_variantannotation_Eigen_PC_raw_rankscore_60ca6617; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_Eigen_PC_raw_rankscore_60ca6617" ON variants_variantannotation USING btree ("Eigen_PC_raw_rankscore");


--
-- Name: variants_variantannotation_Eigen_PC_raw_rankscore_60ca6617_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_Eigen_PC_raw_rankscore_60ca6617_like" ON variants_variantannotation USING btree ("Eigen_PC_raw_rankscore" text_pattern_ops);


--
-- Name: variants_variantannotation_Eigen_phred_7e380c0a; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_Eigen_phred_7e380c0a" ON variants_variantannotation USING btree ("Eigen_phred");


--
-- Name: variants_variantannotation_Eigen_phred_7e380c0a_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_Eigen_phred_7e380c0a_like" ON variants_variantannotation USING btree ("Eigen_phred" text_pattern_ops);


--
-- Name: variants_variantannotation_Eigen_raw_6ab1f960; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_Eigen_raw_6ab1f960" ON variants_variantannotation USING btree ("Eigen_raw");


--
-- Name: variants_variantannotation_Eigen_raw_6ab1f960_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_Eigen_raw_6ab1f960_like" ON variants_variantannotation USING btree ("Eigen_raw" text_pattern_ops);


--
-- Name: variants_variantannotation_Eigen_raw_rankscore_d1bed4a8; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_Eigen_raw_rankscore_d1bed4a8" ON variants_variantannotation USING btree ("Eigen_raw_rankscore");


--
-- Name: variants_variantannotation_Eigen_raw_rankscore_d1bed4a8_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_Eigen_raw_rankscore_d1bed4a8_like" ON variants_variantannotation USING btree ("Eigen_raw_rankscore" text_pattern_ops);


--
-- Name: variants_variantannotation_FATHMM_converted_rankscore_8e20e21a; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_FATHMM_converted_rankscore_8e20e21a" ON variants_variantannotation USING btree ("FATHMM_converted_rankscore");


--
-- Name: variants_variantannotation_FATHMM_pred_29ecfad0; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_FATHMM_pred_29ecfad0" ON variants_variantannotation USING btree ("FATHMM_pred");


--
-- Name: variants_variantannotation_FATHMM_pred_29ecfad0_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_FATHMM_pred_29ecfad0_like" ON variants_variantannotation USING btree ("FATHMM_pred" text_pattern_ops);


--
-- Name: variants_variantannotation_FATHMM_score_bd7ba51e; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_FATHMM_score_bd7ba51e" ON variants_variantannotation USING btree ("FATHMM_score");


--
-- Name: variants_variantannotation_FATHMM_score_bd7ba51e_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_FATHMM_score_bd7ba51e_like" ON variants_variantannotation USING btree ("FATHMM_score" text_pattern_ops);


--
-- Name: variants_variantannotation_GERP_NR_35d0521e; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_GERP_NR_35d0521e" ON variants_variantannotation USING btree ("GERP_NR");


--
-- Name: variants_variantannotation_GERP_NR_35d0521e_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_GERP_NR_35d0521e_like" ON variants_variantannotation USING btree ("GERP_NR" text_pattern_ops);


--
-- Name: variants_variantannotation_GERP_RS_0c324bdc; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_GERP_RS_0c324bdc" ON variants_variantannotation USING btree ("GERP_RS");


--
-- Name: variants_variantannotation_GERP_RS_0c324bdc_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_GERP_RS_0c324bdc_like" ON variants_variantannotation USING btree ("GERP_RS" text_pattern_ops);


--
-- Name: variants_variantannotation_GERP_RS_rankscore_289a81bc; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_GERP_RS_rankscore_289a81bc" ON variants_variantannotation USING btree ("GERP_RS_rankscore");


--
-- Name: variants_variantannotation_GERP_RS_rankscore_289a81bc_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_GERP_RS_rankscore_289a81bc_like" ON variants_variantannotation USING btree ("GERP_RS_rankscore" text_pattern_ops);


--
-- Name: variants_variantannotation_GM12878_confidence_value_b95f3451; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_GM12878_confidence_value_b95f3451" ON variants_variantannotation USING btree ("GM12878_confidence_value");


--
-- Name: variants_variantannotation_GM12878_fitCons_rankscore_c2f322c1; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_GM12878_fitCons_rankscore_c2f322c1" ON variants_variantannotation USING btree ("GM12878_fitCons_rankscore");


--
-- Name: variants_variantannotation_GM12878_fitCons_score_dcbf9d27; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_GM12878_fitCons_score_dcbf9d27" ON variants_variantannotation USING btree ("GM12878_fitCons_score");


--
-- Name: variants_variantannotation_GM12878_fitCons_score_dcbf9d27_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_GM12878_fitCons_score_dcbf9d27_like" ON variants_variantannotation USING btree ("GM12878_fitCons_score" text_pattern_ops);


--
-- Name: variants_variantannotation_GenoCanyon_score_672ed017; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_GenoCanyon_score_672ed017" ON variants_variantannotation USING btree ("GenoCanyon_score");


--
-- Name: variants_variantannotation_GenoCanyon_score_672ed017_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_GenoCanyon_score_672ed017_like" ON variants_variantannotation USING btree ("GenoCanyon_score" text_pattern_ops);


--
-- Name: variants_variantannotation_GenoCanyon_score_rankscore_f58d27db; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_GenoCanyon_score_rankscore_f58d27db" ON variants_variantannotation USING btree ("GenoCanyon_score_rankscore");


--
-- Name: variants_variantannotation_H1_hESC_confidence_value_aa804d36; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_H1_hESC_confidence_value_aa804d36" ON variants_variantannotation USING btree ("H1_hESC_confidence_value");


--
-- Name: variants_variantannotation_H1_hESC_fitCons_rankscore_bfe24fa1; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_H1_hESC_fitCons_rankscore_bfe24fa1" ON variants_variantannotation USING btree ("H1_hESC_fitCons_rankscore");


--
-- Name: variants_variantannotation_H1_hESC_fitCons_score_0348b3c0; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_H1_hESC_fitCons_score_0348b3c0" ON variants_variantannotation USING btree ("H1_hESC_fitCons_score");


--
-- Name: variants_variantannotation_H1_hESC_fitCons_score_0348b3c0_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_H1_hESC_fitCons_score_0348b3c0_like" ON variants_variantannotation USING btree ("H1_hESC_fitCons_score" text_pattern_ops);


--
-- Name: variants_variantannotation_HUVEC_confidence_value_5a8a98c1; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_HUVEC_confidence_value_5a8a98c1" ON variants_variantannotation USING btree ("HUVEC_confidence_value");


--
-- Name: variants_variantannotation_HUVEC_confidence_value_5a8a98c1_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_HUVEC_confidence_value_5a8a98c1_like" ON variants_variantannotation USING btree ("HUVEC_confidence_value" text_pattern_ops);


--
-- Name: variants_variantannotation_HUVEC_fitCons_rankscore_d5a2ea45; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_HUVEC_fitCons_rankscore_d5a2ea45" ON variants_variantannotation USING btree ("HUVEC_fitCons_rankscore");


--
-- Name: variants_variantannotation_HUVEC_fitCons_score_1b294f54; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_HUVEC_fitCons_score_1b294f54" ON variants_variantannotation USING btree ("HUVEC_fitCons_score");


--
-- Name: variants_variantannotation_HUVEC_fitCons_score_1b294f54_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_HUVEC_fitCons_score_1b294f54_like" ON variants_variantannotation USING btree ("HUVEC_fitCons_score" text_pattern_ops);


--
-- Name: variants_variantannotation_LRT_Omega_69381156; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_LRT_Omega_69381156" ON variants_variantannotation USING btree ("LRT_Omega");


--
-- Name: variants_variantannotation_LRT_Omega_69381156_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_LRT_Omega_69381156_like" ON variants_variantannotation USING btree ("LRT_Omega" text_pattern_ops);


--
-- Name: variants_variantannotation_LRT_converted_rankscore_6893c896; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_LRT_converted_rankscore_6893c896" ON variants_variantannotation USING btree ("LRT_converted_rankscore");


--
-- Name: variants_variantannotation_LRT_pred_c98360df; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_LRT_pred_c98360df" ON variants_variantannotation USING btree ("LRT_pred");


--
-- Name: variants_variantannotation_LRT_pred_c98360df_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_LRT_pred_c98360df_like" ON variants_variantannotation USING btree ("LRT_pred" text_pattern_ops);


--
-- Name: variants_variantannotation_LRT_score_629a7f06; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_LRT_score_629a7f06" ON variants_variantannotation USING btree ("LRT_score");


--
-- Name: variants_variantannotation_LRT_score_629a7f06_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_LRT_score_629a7f06_like" ON variants_variantannotation USING btree ("LRT_score" text_pattern_ops);


--
-- Name: variants_variantannotation_MetaLR_pred_f605df6b; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_MetaLR_pred_f605df6b" ON variants_variantannotation USING btree ("MetaLR_pred");


--
-- Name: variants_variantannotation_MetaLR_pred_f605df6b_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_MetaLR_pred_f605df6b_like" ON variants_variantannotation USING btree ("MetaLR_pred" text_pattern_ops);


--
-- Name: variants_variantannotation_MetaLR_rankscore_cc131133; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_MetaLR_rankscore_cc131133" ON variants_variantannotation USING btree ("MetaLR_rankscore");


--
-- Name: variants_variantannotation_MetaLR_rankscore_cc131133_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_MetaLR_rankscore_cc131133_like" ON variants_variantannotation USING btree ("MetaLR_rankscore" text_pattern_ops);


--
-- Name: variants_variantannotation_MetaLR_score_5d29e91d; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_MetaLR_score_5d29e91d" ON variants_variantannotation USING btree ("MetaLR_score");


--
-- Name: variants_variantannotation_MetaLR_score_5d29e91d_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_MetaLR_score_5d29e91d_like" ON variants_variantannotation USING btree ("MetaLR_score" text_pattern_ops);


--
-- Name: variants_variantannotation_MetaSVM_pred_7d01ca7e; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_MetaSVM_pred_7d01ca7e" ON variants_variantannotation USING btree ("MetaSVM_pred");


--
-- Name: variants_variantannotation_MetaSVM_pred_7d01ca7e_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_MetaSVM_pred_7d01ca7e_like" ON variants_variantannotation USING btree ("MetaSVM_pred" text_pattern_ops);


--
-- Name: variants_variantannotation_MetaSVM_rankscore_34b7a9a7; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_MetaSVM_rankscore_34b7a9a7" ON variants_variantannotation USING btree ("MetaSVM_rankscore");


--
-- Name: variants_variantannotation_MetaSVM_rankscore_34b7a9a7_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_MetaSVM_rankscore_34b7a9a7_like" ON variants_variantannotation USING btree ("MetaSVM_rankscore" text_pattern_ops);


--
-- Name: variants_variantannotation_MetaSVM_score_54d56f91; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_MetaSVM_score_54d56f91" ON variants_variantannotation USING btree ("MetaSVM_score");


--
-- Name: variants_variantannotation_MetaSVM_score_54d56f91_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_MetaSVM_score_54d56f91_like" ON variants_variantannotation USING btree ("MetaSVM_score" text_pattern_ops);


--
-- Name: variants_variantannotation_MutationAssessor_UniprotID_74522271; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_MutationAssessor_UniprotID_74522271" ON variants_variantannotation USING btree ("MutationAssessor_UniprotID");


--
-- Name: variants_variantannotation_MutationAssessor_pred_9db3753d; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_MutationAssessor_pred_9db3753d" ON variants_variantannotation USING btree ("MutationAssessor_pred");


--
-- Name: variants_variantannotation_MutationAssessor_pred_9db3753d_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_MutationAssessor_pred_9db3753d_like" ON variants_variantannotation USING btree ("MutationAssessor_pred" text_pattern_ops);


--
-- Name: variants_variantannotation_MutationAssessor_rankscore_49a0066f; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_MutationAssessor_rankscore_49a0066f" ON variants_variantannotation USING btree ("MutationAssessor_rankscore");


--
-- Name: variants_variantannotation_MutationAssessor_score_1122c704; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_MutationAssessor_score_1122c704" ON variants_variantannotation USING btree ("MutationAssessor_score");


--
-- Name: variants_variantannotation_MutationAssessor_score_1122c704_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_MutationAssessor_score_1122c704_like" ON variants_variantannotation USING btree ("MutationAssessor_score" text_pattern_ops);


--
-- Name: variants_variantannotation_MutationAssessor_variant_1d33911f; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_MutationAssessor_variant_1d33911f" ON variants_variantannotation USING btree ("MutationAssessor_variant");


--
-- Name: variants_variantannotation_MutationTaster_AAE_c401f907; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_MutationTaster_AAE_c401f907" ON variants_variantannotation USING btree ("MutationTaster_AAE");


--
-- Name: variants_variantannotation_MutationTaster_AAE_c401f907_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_MutationTaster_AAE_c401f907_like" ON variants_variantannotation USING btree ("MutationTaster_AAE" text_pattern_ops);


--
-- Name: variants_variantannotation_MutationTaster_converted_r_aecc47ab; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_MutationTaster_converted_r_aecc47ab" ON variants_variantannotation USING btree ("MutationTaster_converted_rankscore");


--
-- Name: variants_variantannotation_MutationTaster_model_cd0a7db0; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_MutationTaster_model_cd0a7db0" ON variants_variantannotation USING btree ("MutationTaster_model");


--
-- Name: variants_variantannotation_MutationTaster_model_cd0a7db0_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_MutationTaster_model_cd0a7db0_like" ON variants_variantannotation USING btree ("MutationTaster_model" text_pattern_ops);


--
-- Name: variants_variantannotation_MutationTaster_pred_56fd4418; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_MutationTaster_pred_56fd4418" ON variants_variantannotation USING btree ("MutationTaster_pred");


--
-- Name: variants_variantannotation_MutationTaster_pred_56fd4418_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_MutationTaster_pred_56fd4418_like" ON variants_variantannotation USING btree ("MutationTaster_pred" text_pattern_ops);


--
-- Name: variants_variantannotation_MutationTaster_score_82937080; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_MutationTaster_score_82937080" ON variants_variantannotation USING btree ("MutationTaster_score");


--
-- Name: variants_variantannotation_MutationTaster_score_82937080_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_MutationTaster_score_82937080_like" ON variants_variantannotation USING btree ("MutationTaster_score" text_pattern_ops);


--
-- Name: variants_variantannotation_PROVEAN_converted_rankscore_89206816; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_PROVEAN_converted_rankscore_89206816" ON variants_variantannotation USING btree ("PROVEAN_converted_rankscore");


--
-- Name: variants_variantannotation_PROVEAN_pred_c182ca9b; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_PROVEAN_pred_c182ca9b" ON variants_variantannotation USING btree ("PROVEAN_pred");


--
-- Name: variants_variantannotation_PROVEAN_pred_c182ca9b_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_PROVEAN_pred_c182ca9b_like" ON variants_variantannotation USING btree ("PROVEAN_pred" text_pattern_ops);


--
-- Name: variants_variantannotation_PROVEAN_score_04605cbe; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_PROVEAN_score_04605cbe" ON variants_variantannotation USING btree ("PROVEAN_score");


--
-- Name: variants_variantannotation_PROVEAN_score_04605cbe_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_PROVEAN_score_04605cbe_like" ON variants_variantannotation USING btree ("PROVEAN_score" text_pattern_ops);


--
-- Name: variants_variantannotation_Polyphen2_HDIV_pred_25b5f8be; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_Polyphen2_HDIV_pred_25b5f8be" ON variants_variantannotation USING btree ("Polyphen2_HDIV_pred");


--
-- Name: variants_variantannotation_Polyphen2_HDIV_pred_25b5f8be_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_Polyphen2_HDIV_pred_25b5f8be_like" ON variants_variantannotation USING btree ("Polyphen2_HDIV_pred" text_pattern_ops);


--
-- Name: variants_variantannotation_Polyphen2_HDIV_rankscore_fd0fe3e9; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_Polyphen2_HDIV_rankscore_fd0fe3e9" ON variants_variantannotation USING btree ("Polyphen2_HDIV_rankscore");


--
-- Name: variants_variantannotation_Polyphen2_HDIV_score_7240438a; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_Polyphen2_HDIV_score_7240438a" ON variants_variantannotation USING btree ("Polyphen2_HDIV_score");


--
-- Name: variants_variantannotation_Polyphen2_HDIV_score_7240438a_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_Polyphen2_HDIV_score_7240438a_like" ON variants_variantannotation USING btree ("Polyphen2_HDIV_score" text_pattern_ops);


--
-- Name: variants_variantannotation_Polyphen2_HVAR_pred_3cb67de2; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_Polyphen2_HVAR_pred_3cb67de2" ON variants_variantannotation USING btree ("Polyphen2_HVAR_pred");


--
-- Name: variants_variantannotation_Polyphen2_HVAR_pred_3cb67de2_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_Polyphen2_HVAR_pred_3cb67de2_like" ON variants_variantannotation USING btree ("Polyphen2_HVAR_pred" text_pattern_ops);


--
-- Name: variants_variantannotation_Polyphen2_HVAR_rankscore_d1b0c147; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_Polyphen2_HVAR_rankscore_d1b0c147" ON variants_variantannotation USING btree ("Polyphen2_HVAR_rankscore");


--
-- Name: variants_variantannotation_Polyphen2_HVAR_score_3df93675; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_Polyphen2_HVAR_score_3df93675" ON variants_variantannotation USING btree ("Polyphen2_HVAR_score");


--
-- Name: variants_variantannotation_Polyphen2_HVAR_score_3df93675_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_Polyphen2_HVAR_score_3df93675_like" ON variants_variantannotation USING btree ("Polyphen2_HVAR_score" text_pattern_ops);


--
-- Name: variants_variantannotation_Reliability_index_63a1a2a1; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_Reliability_index_63a1a2a1" ON variants_variantannotation USING btree ("Reliability_index");


--
-- Name: variants_variantannotation_Reliability_index_63a1a2a1_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_Reliability_index_63a1a2a1_like" ON variants_variantannotation USING btree ("Reliability_index" text_pattern_ops);


--
-- Name: variants_variantannotation_SIFT_converted_rankscore_e6284979; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_SIFT_converted_rankscore_e6284979" ON variants_variantannotation USING btree ("SIFT_converted_rankscore");


--
-- Name: variants_variantannotation_SIFT_score_40b5b7a5; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_SIFT_score_40b5b7a5" ON variants_variantannotation USING btree ("SIFT_score");


--
-- Name: variants_variantannotation_SIFT_score_40b5b7a5_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_SIFT_score_40b5b7a5_like" ON variants_variantannotation USING btree ("SIFT_score" text_pattern_ops);


--
-- Name: variants_variantannotation_SiPhy_29way_logOdds_04011feb; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_SiPhy_29way_logOdds_04011feb" ON variants_variantannotation USING btree ("SiPhy_29way_logOdds");


--
-- Name: variants_variantannotation_SiPhy_29way_logOdds_04011feb_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_SiPhy_29way_logOdds_04011feb_like" ON variants_variantannotation USING btree ("SiPhy_29way_logOdds" text_pattern_ops);


--
-- Name: variants_variantannotation_SiPhy_29way_logOdds_ranksc_17078f4d; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_SiPhy_29way_logOdds_ranksc_17078f4d" ON variants_variantannotation USING btree ("SiPhy_29way_logOdds_rankscore");


--
-- Name: variants_variantannotation_SiPhy_29way_pi_0bf68d7c; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_SiPhy_29way_pi_0bf68d7c" ON variants_variantannotation USING btree ("SiPhy_29way_pi");


--
-- Name: variants_variantannotation_SiPhy_29way_pi_0bf68d7c_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_SiPhy_29way_pi_0bf68d7c_like" ON variants_variantannotation USING btree ("SiPhy_29way_pi" text_pattern_ops);


--
-- Name: variants_variantannotation_Transcript_id_VEST3_835ad617; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_Transcript_id_VEST3_835ad617" ON variants_variantannotation USING btree ("Transcript_id_VEST3");


--
-- Name: variants_variantannotation_Transcript_id_VEST3_835ad617_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_Transcript_id_VEST3_835ad617_like" ON variants_variantannotation USING btree ("Transcript_id_VEST3" text_pattern_ops);


--
-- Name: variants_variantannotation_Transcript_var_VEST3_ad2bdffe; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_Transcript_var_VEST3_ad2bdffe" ON variants_variantannotation USING btree ("Transcript_var_VEST3");


--
-- Name: variants_variantannotation_Transcript_var_VEST3_ad2bdffe_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_Transcript_var_VEST3_ad2bdffe_like" ON variants_variantannotation USING btree ("Transcript_var_VEST3" text_pattern_ops);


--
-- Name: variants_variantannotation_Uniprot_aapos_Polyphen2_90ecae1a; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_Uniprot_aapos_Polyphen2_90ecae1a" ON variants_variantannotation USING btree ("Uniprot_aapos_Polyphen2");


--
-- Name: variants_variantannotation_Uniprot_acc_Polyphen2_75af2304; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_Uniprot_acc_Polyphen2_75af2304" ON variants_variantannotation USING btree ("Uniprot_acc_Polyphen2");


--
-- Name: variants_variantannotation_Uniprot_acc_Polyphen2_75af2304_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_Uniprot_acc_Polyphen2_75af2304_like" ON variants_variantannotation USING btree ("Uniprot_acc_Polyphen2" text_pattern_ops);


--
-- Name: variants_variantannotation_Uniprot_id_Polyphen2_f6e4037d; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_Uniprot_id_Polyphen2_f6e4037d" ON variants_variantannotation USING btree ("Uniprot_id_Polyphen2");


--
-- Name: variants_variantannotation_Uniprot_id_Polyphen2_f6e4037d_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_Uniprot_id_Polyphen2_f6e4037d_like" ON variants_variantannotation USING btree ("Uniprot_id_Polyphen2" text_pattern_ops);


--
-- Name: variants_variantannotation_VEST3_rankscore_7cb68a48; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_VEST3_rankscore_7cb68a48" ON variants_variantannotation USING btree ("VEST3_rankscore");


--
-- Name: variants_variantannotation_VEST3_rankscore_7cb68a48_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_VEST3_rankscore_7cb68a48_like" ON variants_variantannotation USING btree ("VEST3_rankscore" text_pattern_ops);


--
-- Name: variants_variantannotation_VEST3_score_3a337001; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_VEST3_score_3a337001" ON variants_variantannotation USING btree ("VEST3_score");


--
-- Name: variants_variantannotation_VEST3_score_3a337001_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_VEST3_score_3a337001_like" ON variants_variantannotation USING btree ("VEST3_score" text_pattern_ops);


--
-- Name: variants_variantannotation_alt_b0e40df9; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variantannotation_alt_b0e40df9 ON variants_variantannotation USING btree (alt);


--
-- Name: variants_variantannotation_alt_b0e40df9_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variantannotation_alt_b0e40df9_like ON variants_variantannotation USING btree (alt text_pattern_ops);


--
-- Name: variants_variantannotation_cadd_37bf481a; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variantannotation_cadd_37bf481a ON variants_variantannotation USING btree (cadd);


--
-- Name: variants_variantannotation_clinvar_CLNSRC_bdf60e13; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_clinvar_CLNSRC_bdf60e13" ON variants_variantannotation USING btree ("clinvar_CLNSRC");


--
-- Name: variants_variantannotation_clinvar_CLNSRC_bdf60e13_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_clinvar_CLNSRC_bdf60e13_like" ON variants_variantannotation USING btree ("clinvar_CLNSRC" text_pattern_ops);


--
-- Name: variants_variantannotation_clinvar_clnsig_259ff9a7; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variantannotation_clinvar_clnsig_259ff9a7 ON variants_variantannotation USING btree (clinvar_clnsig);


--
-- Name: variants_variantannotation_clinvar_clnsig_259ff9a7_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variantannotation_clinvar_clnsig_259ff9a7_like ON variants_variantannotation USING btree (clinvar_clnsig text_pattern_ops);


--
-- Name: variants_variantannotation_clinvar_golden_stars_c288f86b; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variantannotation_clinvar_golden_stars_c288f86b ON variants_variantannotation USING btree (clinvar_golden_stars);


--
-- Name: variants_variantannotation_clinvar_golden_stars_c288f86b_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variantannotation_clinvar_golden_stars_c288f86b_like ON variants_variantannotation USING btree (clinvar_golden_stars text_pattern_ops);


--
-- Name: variants_variantannotation_clinvar_rs_1255a5f9; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variantannotation_clinvar_rs_1255a5f9 ON variants_variantannotation USING btree (clinvar_rs);


--
-- Name: variants_variantannotation_clinvar_rs_1255a5f9_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variantannotation_clinvar_rs_1255a5f9_like ON variants_variantannotation USING btree (clinvar_rs text_pattern_ops);


--
-- Name: variants_variantannotation_clinvar_trait_829342d7; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variantannotation_clinvar_trait_829342d7 ON variants_variantannotation USING btree (clinvar_trait);


--
-- Name: variants_variantannotation_clinvar_trait_829342d7_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variantannotation_clinvar_trait_829342d7_like ON variants_variantannotation USING btree (clinvar_trait text_pattern_ops);


--
-- Name: variants_variantannotation_condel_131c9e5f; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variantannotation_condel_131c9e5f ON variants_variantannotation USING btree (condel);


--
-- Name: variants_variantannotation_condel_pred_46c964c2; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variantannotation_condel_pred_46c964c2 ON variants_variantannotation USING btree (condel_pred);


--
-- Name: variants_variantannotation_condel_pred_46c964c2_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variantannotation_condel_pred_46c964c2_like ON variants_variantannotation USING btree (condel_pred text_pattern_ops);


--
-- Name: variants_variantannotation_dann_adc03dfa; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variantannotation_dann_adc03dfa ON variants_variantannotation USING btree (dann);


--
-- Name: variants_variantannotation_dbsnp_build_e0253b23; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variantannotation_dbsnp_build_e0253b23 ON variants_variantannotation USING btree (dbsnp_build);


--
-- Name: variants_variantannotation_dbsnp_maf_f8392769; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variantannotation_dbsnp_maf_f8392769 ON variants_variantannotation USING btree (dbsnp_maf);


--
-- Name: variants_variantannotation_ensembl_clin_HGMD_3cdf4355; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_ensembl_clin_HGMD_3cdf4355" ON variants_variantannotation USING btree ("ensembl_clin_HGMD");


--
-- Name: variants_variantannotation_esp_maf_8b73f960; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variantannotation_esp_maf_8b73f960 ON variants_variantannotation USING btree (esp_maf);


--
-- Name: variants_variantannotation_fathmm_MKL_coding_group_e8ac587b; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_fathmm_MKL_coding_group_e8ac587b" ON variants_variantannotation USING btree ("fathmm_MKL_coding_group");


--
-- Name: variants_variantannotation_fathmm_MKL_coding_pred_5d2ced76; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_fathmm_MKL_coding_pred_5d2ced76" ON variants_variantannotation USING btree ("fathmm_MKL_coding_pred");


--
-- Name: variants_variantannotation_fathmm_MKL_coding_pred_5d2ced76_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_fathmm_MKL_coding_pred_5d2ced76_like" ON variants_variantannotation USING btree ("fathmm_MKL_coding_pred" text_pattern_ops);


--
-- Name: variants_variantannotation_fathmm_MKL_coding_rankscore_7f0a15b6; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_fathmm_MKL_coding_rankscore_7f0a15b6" ON variants_variantannotation USING btree ("fathmm_MKL_coding_rankscore");


--
-- Name: variants_variantannotation_fathmm_MKL_coding_score_55a6a0ff; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_fathmm_MKL_coding_score_55a6a0ff" ON variants_variantannotation USING btree ("fathmm_MKL_coding_score");


--
-- Name: variants_variantannotation_filter_c3306a99; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variantannotation_filter_c3306a99 ON variants_variantannotation USING btree (filter);


--
-- Name: variants_variantannotation_filter_c3306a99_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variantannotation_filter_c3306a99_like ON variants_variantannotation USING btree (filter text_pattern_ops);


--
-- Name: variants_variantannotation_format_38724ac0; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variantannotation_format_38724ac0 ON variants_variantannotation USING btree (format);


--
-- Name: variants_variantannotation_format_38724ac0_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variantannotation_format_38724ac0_like ON variants_variantannotation USING btree (format text_pattern_ops);


--
-- Name: variants_variantannotation_gene_a78f1332; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variantannotation_gene_a78f1332 ON variants_variantannotation USING btree (gene);


--
-- Name: variants_variantannotation_gene_a78f1332_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variantannotation_gene_a78f1332_like ON variants_variantannotation USING btree (gene text_pattern_ops);


--
-- Name: variants_variantannotation_genomes1k_maf_e45351dc; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variantannotation_genomes1k_maf_e45351dc ON variants_variantannotation USING btree (genomes1k_maf);


--
-- Name: variants_variantannotation_genotype_00bad34d; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variantannotation_genotype_00bad34d ON variants_variantannotation USING btree (genotype);


--
-- Name: variants_variantannotation_genotype_00bad34d_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variantannotation_genotype_00bad34d_like ON variants_variantannotation USING btree (genotype text_pattern_ops);


--
-- Name: variants_variantannotation_genotype_col_5d966251; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variantannotation_genotype_col_5d966251 ON variants_variantannotation USING btree (genotype_col);


--
-- Name: variants_variantannotation_genotype_col_5d966251_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variantannotation_genotype_col_5d966251_like ON variants_variantannotation USING btree (genotype_col text_pattern_ops);


--
-- Name: variants_variantannotation_hgmd_entries_daddb45a; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variantannotation_hgmd_entries_daddb45a ON variants_variantannotation USING btree (hgmd_entries);


--
-- Name: variants_variantannotation_hgmd_entries_daddb45a_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variantannotation_hgmd_entries_daddb45a_like ON variants_variantannotation USING btree (hgmd_entries text_pattern_ops);


--
-- Name: variants_variantannotation_hi_index_28d25c66; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variantannotation_hi_index_28d25c66 ON variants_variantannotation USING btree (hi_index);


--
-- Name: variants_variantannotation_hi_index_perc_29907738; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variantannotation_hi_index_perc_29907738 ON variants_variantannotation USING btree (hi_index_perc);


--
-- Name: variants_variantannotation_hi_index_str_d70e1e47; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variantannotation_hi_index_str_d70e1e47 ON variants_variantannotation USING btree (hi_index_str);


--
-- Name: variants_variantannotation_hi_index_str_d70e1e47_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variantannotation_hi_index_str_d70e1e47_like ON variants_variantannotation USING btree (hi_index_str text_pattern_ops);


--
-- Name: variants_variantannotation_integrated_confidence_value_45c8c0b0; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variantannotation_integrated_confidence_value_45c8c0b0 ON variants_variantannotation USING btree (integrated_confidence_value);


--
-- Name: variants_variantannotation_integrated_fitCons_ranksco_bd92809e; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_integrated_fitCons_ranksco_bd92809e" ON variants_variantannotation USING btree ("integrated_fitCons_rankscore");


--
-- Name: variants_variantannotation_integrated_fitCons_score_91425982; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_integrated_fitCons_score_91425982" ON variants_variantannotation USING btree ("integrated_fitCons_score");


--
-- Name: variants_variantannotation_is_at_hgmd_5ef7d1bf; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variantannotation_is_at_hgmd_5ef7d1bf ON variants_variantannotation USING btree (is_at_hgmd);


--
-- Name: variants_variantannotation_is_at_omim_38fa43f4; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variantannotation_is_at_omim_38fa43f4 ON variants_variantannotation USING btree (is_at_omim);


--
-- Name: variants_variantannotation_mcap_pred_db374520; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variantannotation_mcap_pred_db374520 ON variants_variantannotation USING btree (mcap_pred);


--
-- Name: variants_variantannotation_mcap_pred_db374520_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variantannotation_mcap_pred_db374520_like ON variants_variantannotation USING btree (mcap_pred text_pattern_ops);


--
-- Name: variants_variantannotation_mcap_rankscore_e31886db; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variantannotation_mcap_rankscore_e31886db ON variants_variantannotation USING btree (mcap_rankscore);


--
-- Name: variants_variantannotation_mcap_score_4ca611ba; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variantannotation_mcap_score_4ca611ba ON variants_variantannotation USING btree (mcap_score);


--
-- Name: variants_variantannotation_mutation_type_70d4b7fb; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variantannotation_mutation_type_70d4b7fb ON variants_variantannotation USING btree (mutation_type);


--
-- Name: variants_variantannotation_mutation_type_70d4b7fb_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variantannotation_mutation_type_70d4b7fb_like ON variants_variantannotation USING btree (mutation_type text_pattern_ops);


--
-- Name: variants_variantannotation_phastCons100way_vertebrate_0fc58510; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_phastCons100way_vertebrate_0fc58510" ON variants_variantannotation USING btree ("phastCons100way_vertebrate_rankscore");


--
-- Name: variants_variantannotation_phastCons100way_vertebrate_9e2f68b8; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_phastCons100way_vertebrate_9e2f68b8" ON variants_variantannotation USING btree ("phastCons100way_vertebrate");


--
-- Name: variants_variantannotation_phastCons20way_mammalian_b5d6ff44; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_phastCons20way_mammalian_b5d6ff44" ON variants_variantannotation USING btree ("phastCons20way_mammalian");


--
-- Name: variants_variantannotation_phastCons20way_mammalian_r_df6cf11f; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_phastCons20way_mammalian_r_df6cf11f" ON variants_variantannotation USING btree ("phastCons20way_mammalian_rankscore");


--
-- Name: variants_variantannotation_phyloP100way_vertebrate_8d5ebe4e; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_phyloP100way_vertebrate_8d5ebe4e" ON variants_variantannotation USING btree ("phyloP100way_vertebrate");


--
-- Name: variants_variantannotation_phyloP100way_vertebrate_ra_962a58b5; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_phyloP100way_vertebrate_ra_962a58b5" ON variants_variantannotation USING btree ("phyloP100way_vertebrate_rankscore");


--
-- Name: variants_variantannotation_phyloP20way_mammalian_66327d6a; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_phyloP20way_mammalian_66327d6a" ON variants_variantannotation USING btree ("phyloP20way_mammalian");


--
-- Name: variants_variantannotation_phyloP20way_mammalian_66327d6a_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_phyloP20way_mammalian_66327d6a_like" ON variants_variantannotation USING btree ("phyloP20way_mammalian" text_pattern_ops);


--
-- Name: variants_variantannotation_phyloP20way_mammalian_rank_244316c3; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX "variants_variantannotation_phyloP20way_mammalian_rank_244316c3" ON variants_variantannotation USING btree ("phyloP20way_mammalian_rankscore");


--
-- Name: variants_variantannotation_polyphen2_ffc8d51b; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variantannotation_polyphen2_ffc8d51b ON variants_variantannotation USING btree (polyphen2);


--
-- Name: variants_variantannotation_polyphen2_pred_05bf0a89; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variantannotation_polyphen2_pred_05bf0a89 ON variants_variantannotation USING btree (polyphen2_pred);


--
-- Name: variants_variantannotation_polyphen2_pred_05bf0a89_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variantannotation_polyphen2_pred_05bf0a89_like ON variants_variantannotation USING btree (polyphen2_pred text_pattern_ops);


--
-- Name: variants_variantannotation_qual_38f872a6; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variantannotation_qual_38f872a6 ON variants_variantannotation USING btree (qual);


--
-- Name: variants_variantannotation_ref_bb53eba9; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variantannotation_ref_bb53eba9 ON variants_variantannotation USING btree (ref);


--
-- Name: variants_variantannotation_ref_bb53eba9_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variantannotation_ref_bb53eba9_like ON variants_variantannotation USING btree (ref text_pattern_ops);


--
-- Name: variants_variantannotation_revel_score_893cfa48; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variantannotation_revel_score_893cfa48 ON variants_variantannotation USING btree (revel_score);


--
-- Name: variants_variantannotation_revel_score_893cfa48_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variantannotation_revel_score_893cfa48_like ON variants_variantannotation USING btree (revel_score text_pattern_ops);


--
-- Name: variants_variantannotation_sift_0b4f1756; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variantannotation_sift_0b4f1756 ON variants_variantannotation USING btree (sift);


--
-- Name: variants_variantannotation_sift_pred_231d1fce; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variantannotation_sift_pred_231d1fce ON variants_variantannotation USING btree (sift_pred);


--
-- Name: variants_variantannotation_sift_pred_231d1fce_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variantannotation_sift_pred_231d1fce_like ON variants_variantannotation USING btree (sift_pred text_pattern_ops);


--
-- Name: variants_variantannotation_snpeff_aa_change_c8b1064a; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variantannotation_snpeff_aa_change_c8b1064a ON variants_variantannotation USING btree (snpeff_aa_change);


--
-- Name: variants_variantannotation_snpeff_aa_change_c8b1064a_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variantannotation_snpeff_aa_change_c8b1064a_like ON variants_variantannotation USING btree (snpeff_aa_change text_pattern_ops);


--
-- Name: variants_variantannotation_snpeff_biotype_0b95504a; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variantannotation_snpeff_biotype_0b95504a ON variants_variantannotation USING btree (snpeff_biotype);


--
-- Name: variants_variantannotation_snpeff_biotype_0b95504a_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variantannotation_snpeff_biotype_0b95504a_like ON variants_variantannotation USING btree (snpeff_biotype text_pattern_ops);


--
-- Name: variants_variantannotation_snpeff_codon_change_fa81f3a1; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variantannotation_snpeff_codon_change_fa81f3a1 ON variants_variantannotation USING btree (snpeff_codon_change);


--
-- Name: variants_variantannotation_snpeff_codon_change_fa81f3a1_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variantannotation_snpeff_codon_change_fa81f3a1_like ON variants_variantannotation USING btree (snpeff_codon_change text_pattern_ops);


--
-- Name: variants_variantannotation_snpeff_effect_4514b685; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variantannotation_snpeff_effect_4514b685 ON variants_variantannotation USING btree (snpeff_effect);


--
-- Name: variants_variantannotation_snpeff_effect_4514b685_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variantannotation_snpeff_effect_4514b685_like ON variants_variantannotation USING btree (snpeff_effect text_pattern_ops);


--
-- Name: variants_variantannotation_snpeff_exon_rank_a1bbb473; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variantannotation_snpeff_exon_rank_a1bbb473 ON variants_variantannotation USING btree (snpeff_exon_rank);


--
-- Name: variants_variantannotation_snpeff_exon_rank_a1bbb473_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variantannotation_snpeff_exon_rank_a1bbb473_like ON variants_variantannotation USING btree (snpeff_exon_rank text_pattern_ops);


--
-- Name: variants_variantannotation_snpeff_func_class_5dddd175; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variantannotation_snpeff_func_class_5dddd175 ON variants_variantannotation USING btree (snpeff_func_class);


--
-- Name: variants_variantannotation_snpeff_func_class_5dddd175_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variantannotation_snpeff_func_class_5dddd175_like ON variants_variantannotation USING btree (snpeff_func_class text_pattern_ops);


--
-- Name: variants_variantannotation_snpeff_gene_coding_ca30a8c2; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variantannotation_snpeff_gene_coding_ca30a8c2 ON variants_variantannotation USING btree (snpeff_gene_coding);


--
-- Name: variants_variantannotation_snpeff_gene_coding_ca30a8c2_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variantannotation_snpeff_gene_coding_ca30a8c2_like ON variants_variantannotation USING btree (snpeff_gene_coding text_pattern_ops);


--
-- Name: variants_variantannotation_snpeff_gene_name_a1365580; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variantannotation_snpeff_gene_name_a1365580 ON variants_variantannotation USING btree (snpeff_gene_name);


--
-- Name: variants_variantannotation_snpeff_gene_name_a1365580_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variantannotation_snpeff_gene_name_a1365580_like ON variants_variantannotation USING btree (snpeff_gene_name text_pattern_ops);


--
-- Name: variants_variantannotation_snpeff_impact_c1b57b9e; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variantannotation_snpeff_impact_c1b57b9e ON variants_variantannotation USING btree (snpeff_impact);


--
-- Name: variants_variantannotation_snpeff_impact_c1b57b9e_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variantannotation_snpeff_impact_c1b57b9e_like ON variants_variantannotation USING btree (snpeff_impact text_pattern_ops);


--
-- Name: variants_variantannotation_snpeff_transcript_id_750b677c; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variantannotation_snpeff_transcript_id_750b677c ON variants_variantannotation USING btree (snpeff_transcript_id);


--
-- Name: variants_variantannotation_snpeff_transcript_id_750b677c_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variantannotation_snpeff_transcript_id_750b677c_like ON variants_variantannotation USING btree (snpeff_transcript_id text_pattern_ops);


--
-- Name: variants_variantannotation_variant_id_b672d38c; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variantannotation_variant_id_b672d38c ON variants_variantannotation USING btree (variant_id);


--
-- Name: variants_variantannotation_variant_id_b672d38c_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variantannotation_variant_id_b672d38c_like ON variants_variantannotation USING btree (variant_id text_pattern_ops);


--
-- Name: variants_variantannotation_vartype_c6b7cef4; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variantannotation_vartype_c6b7cef4 ON variants_variantannotation USING btree (vartype);


--
-- Name: variants_variantannotation_vartype_c6b7cef4_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variantannotation_vartype_c6b7cef4_like ON variants_variantannotation USING btree (vartype text_pattern_ops);


--
-- Name: variants_variantannotation_vep_allele_b7b17ccf; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variantannotation_vep_allele_b7b17ccf ON variants_variantannotation USING btree (vep_allele);


--
-- Name: variants_variantannotation_vep_allele_b7b17ccf_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variantannotation_vep_allele_b7b17ccf_like ON variants_variantannotation USING btree (vep_allele text_pattern_ops);


--
-- Name: variants_variantannotation_vep_amino_acids_c3d8c98a; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variantannotation_vep_amino_acids_c3d8c98a ON variants_variantannotation USING btree (vep_amino_acids);


--
-- Name: variants_variantannotation_vep_amino_acids_c3d8c98a_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variantannotation_vep_amino_acids_c3d8c98a_like ON variants_variantannotation USING btree (vep_amino_acids text_pattern_ops);


--
-- Name: variants_variantannotation_vep_cdna_position_da7e7241; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variantannotation_vep_cdna_position_da7e7241 ON variants_variantannotation USING btree (vep_cdna_position);


--
-- Name: variants_variantannotation_vep_cdna_position_da7e7241_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variantannotation_vep_cdna_position_da7e7241_like ON variants_variantannotation USING btree (vep_cdna_position text_pattern_ops);


--
-- Name: variants_variantannotation_vep_cds_position_6857fe60; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variantannotation_vep_cds_position_6857fe60 ON variants_variantannotation USING btree (vep_cds_position);


--
-- Name: variants_variantannotation_vep_cds_position_6857fe60_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variantannotation_vep_cds_position_6857fe60_like ON variants_variantannotation USING btree (vep_cds_position text_pattern_ops);


--
-- Name: variants_variantannotation_vep_codons_b3b5b846; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variantannotation_vep_codons_b3b5b846 ON variants_variantannotation USING btree (vep_codons);


--
-- Name: variants_variantannotation_vep_codons_b3b5b846_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variantannotation_vep_codons_b3b5b846_like ON variants_variantannotation USING btree (vep_codons text_pattern_ops);


--
-- Name: variants_variantannotation_vep_condel_199119a5; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variantannotation_vep_condel_199119a5 ON variants_variantannotation USING btree (vep_condel);


--
-- Name: variants_variantannotation_vep_condel_199119a5_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variantannotation_vep_condel_199119a5_like ON variants_variantannotation USING btree (vep_condel text_pattern_ops);


--
-- Name: variants_variantannotation_vep_consequence_027494c0; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variantannotation_vep_consequence_027494c0 ON variants_variantannotation USING btree (vep_consequence);


--
-- Name: variants_variantannotation_vep_consequence_027494c0_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variantannotation_vep_consequence_027494c0_like ON variants_variantannotation USING btree (vep_consequence text_pattern_ops);


--
-- Name: variants_variantannotation_vep_distance_ce5e04a3; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variantannotation_vep_distance_ce5e04a3 ON variants_variantannotation USING btree (vep_distance);


--
-- Name: variants_variantannotation_vep_distance_ce5e04a3_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variantannotation_vep_distance_ce5e04a3_like ON variants_variantannotation USING btree (vep_distance text_pattern_ops);


--
-- Name: variants_variantannotation_vep_existing_variation_805590bc; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variantannotation_vep_existing_variation_805590bc ON variants_variantannotation USING btree (vep_existing_variation);


--
-- Name: variants_variantannotation_vep_existing_variation_805590bc_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variantannotation_vep_existing_variation_805590bc_like ON variants_variantannotation USING btree (vep_existing_variation text_pattern_ops);


--
-- Name: variants_variantannotation_vep_feature_b843f5be; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variantannotation_vep_feature_b843f5be ON variants_variantannotation USING btree (vep_feature);


--
-- Name: variants_variantannotation_vep_feature_b843f5be_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variantannotation_vep_feature_b843f5be_like ON variants_variantannotation USING btree (vep_feature text_pattern_ops);


--
-- Name: variants_variantannotation_vep_feature_type_ae212047; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variantannotation_vep_feature_type_ae212047 ON variants_variantannotation USING btree (vep_feature_type);


--
-- Name: variants_variantannotation_vep_feature_type_ae212047_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variantannotation_vep_feature_type_ae212047_like ON variants_variantannotation USING btree (vep_feature_type text_pattern_ops);


--
-- Name: variants_variantannotation_vep_gene_6e7b6654; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variantannotation_vep_gene_6e7b6654 ON variants_variantannotation USING btree (vep_gene);


--
-- Name: variants_variantannotation_vep_gene_6e7b6654_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variantannotation_vep_gene_6e7b6654_like ON variants_variantannotation USING btree (vep_gene text_pattern_ops);


--
-- Name: variants_variantannotation_vep_polyphen_fd623122; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variantannotation_vep_polyphen_fd623122 ON variants_variantannotation USING btree (vep_polyphen);


--
-- Name: variants_variantannotation_vep_polyphen_fd623122_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variantannotation_vep_polyphen_fd623122_like ON variants_variantannotation USING btree (vep_polyphen text_pattern_ops);


--
-- Name: variants_variantannotation_vep_protein_position_84ddfdfe; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variantannotation_vep_protein_position_84ddfdfe ON variants_variantannotation USING btree (vep_protein_position);


--
-- Name: variants_variantannotation_vep_protein_position_84ddfdfe_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variantannotation_vep_protein_position_84ddfdfe_like ON variants_variantannotation USING btree (vep_protein_position text_pattern_ops);


--
-- Name: variants_variantannotation_vep_sift_438b9d70; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variantannotation_vep_sift_438b9d70 ON variants_variantannotation USING btree (vep_sift);


--
-- Name: variants_variantannotation_vep_sift_438b9d70_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variantannotation_vep_sift_438b9d70_like ON variants_variantannotation USING btree (vep_sift text_pattern_ops);


--
-- Name: variants_variantannotation_vep_strand_23effb29; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variantannotation_vep_strand_23effb29 ON variants_variantannotation USING btree (vep_strand);


--
-- Name: variants_variantannotation_vep_strand_23effb29_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variantannotation_vep_strand_23effb29_like ON variants_variantannotation USING btree (vep_strand text_pattern_ops);


--
-- Name: variants_variantannotation_vep_symbol_b55d5119; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variantannotation_vep_symbol_b55d5119 ON variants_variantannotation USING btree (vep_symbol);


--
-- Name: variants_variantannotation_vep_symbol_b55d5119_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variantannotation_vep_symbol_b55d5119_like ON variants_variantannotation USING btree (vep_symbol text_pattern_ops);


--
-- Name: variants_variantannotation_vep_symbol_source_5f6901b0; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variantannotation_vep_symbol_source_5f6901b0 ON variants_variantannotation USING btree (vep_symbol_source);


--
-- Name: variants_variantannotation_vep_symbol_source_5f6901b0_like; Type: INDEX; Schema: public; Owner: raony
--

CREATE INDEX variants_variantannotation_vep_symbol_source_5f6901b0_like ON variants_variantannotation USING btree (vep_symbol_source text_pattern_ops);


--
-- Name: account_emailaddress account_emailaddress_user_id_2c513194_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY account_emailaddress
    ADD CONSTRAINT account_emailaddress_user_id_2c513194_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: account_emailconfirmation account_emailconfirm_email_address_id_5b7f8c58_fk_account_e; Type: FK CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY account_emailconfirmation
    ADD CONSTRAINT account_emailconfirm_email_address_id_5b7f8c58_fk_account_e FOREIGN KEY (email_address_id) REFERENCES account_emailaddress(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permissio_permission_id_84c5c92e_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permissions_group_id_b120cbf9_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_permission auth_permission_content_type_id_2f476e4b_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups auth_user_groups_group_id_97559544_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_group_id_97559544_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups auth_user_groups_user_id_6a12ed8b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_6a12ed8b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cases_case_case_groups cases_case_case_groups_case_id_2c56addb_fk_cases_case_id; Type: FK CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY cases_case_case_groups
    ADD CONSTRAINT cases_case_case_groups_case_id_2c56addb_fk_cases_case_id FOREIGN KEY (case_id) REFERENCES cases_case(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cases_case_case_groups cases_case_case_groups_group_id_2d600616_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY cases_case_case_groups
    ADD CONSTRAINT cases_case_case_groups_group_id_2d600616_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cases_case_cases cases_case_cases_case_id_90e8cfc0_fk_cases_case_id; Type: FK CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY cases_case_cases
    ADD CONSTRAINT cases_case_cases_case_id_90e8cfc0_fk_cases_case_id FOREIGN KEY (case_id) REFERENCES cases_case(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cases_case_cases cases_case_cases_individual_id_359c652b_fk_individua; Type: FK CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY cases_case_cases
    ADD CONSTRAINT cases_case_cases_individual_id_359c652b_fk_individua FOREIGN KEY (individual_id) REFERENCES individuals_individual(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cases_case_children cases_case_children_case_id_c6e7d0f9_fk_cases_case_id; Type: FK CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY cases_case_children
    ADD CONSTRAINT cases_case_children_case_id_c6e7d0f9_fk_cases_case_id FOREIGN KEY (case_id) REFERENCES cases_case(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cases_case_children cases_case_children_individual_id_548cbcd1_fk_individua; Type: FK CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY cases_case_children
    ADD CONSTRAINT cases_case_children_individual_id_548cbcd1_fk_individua FOREIGN KEY (individual_id) REFERENCES individuals_individual(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cases_case_control_groups cases_case_control_groups_case_id_a1d0d7d0_fk_cases_case_id; Type: FK CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY cases_case_control_groups
    ADD CONSTRAINT cases_case_control_groups_case_id_a1d0d7d0_fk_cases_case_id FOREIGN KEY (case_id) REFERENCES cases_case(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cases_case_control_groups cases_case_control_groups_group_id_6c361188_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY cases_case_control_groups
    ADD CONSTRAINT cases_case_control_groups_group_id_6c361188_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cases_case_controls cases_case_controls_case_id_ce379262_fk_cases_case_id; Type: FK CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY cases_case_controls
    ADD CONSTRAINT cases_case_controls_case_id_ce379262_fk_cases_case_id FOREIGN KEY (case_id) REFERENCES cases_case(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cases_case_controls cases_case_controls_individual_id_b3771c33_fk_individua; Type: FK CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY cases_case_controls
    ADD CONSTRAINT cases_case_controls_individual_id_b3771c33_fk_individua FOREIGN KEY (individual_id) REFERENCES individuals_individual(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cases_case cases_case_father_id_d3aa9ff7_fk_individuals_individual_id; Type: FK CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY cases_case
    ADD CONSTRAINT cases_case_father_id_d3aa9ff7_fk_individuals_individual_id FOREIGN KEY (father_id) REFERENCES individuals_individual(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cases_case cases_case_mother_id_60214b94_fk_individuals_individual_id; Type: FK CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY cases_case
    ADD CONSTRAINT cases_case_mother_id_60214b94_fk_individuals_individual_id FOREIGN KEY (mother_id) REFERENCES individuals_individual(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cases_case_shared_with_groups cases_case_shared_wi_group_id_eff5b712_fk_auth_grou; Type: FK CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY cases_case_shared_with_groups
    ADD CONSTRAINT cases_case_shared_wi_group_id_eff5b712_fk_auth_grou FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cases_case_shared_with_groups cases_case_shared_with_groups_case_id_b4d253d9_fk_cases_case_id; Type: FK CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY cases_case_shared_with_groups
    ADD CONSTRAINT cases_case_shared_with_groups_case_id_b4d253d9_fk_cases_case_id FOREIGN KEY (case_id) REFERENCES cases_case(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cases_case_shared_with_users cases_case_shared_with_users_case_id_c4a1f778_fk_cases_case_id; Type: FK CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY cases_case_shared_with_users
    ADD CONSTRAINT cases_case_shared_with_users_case_id_c4a1f778_fk_cases_case_id FOREIGN KEY (case_id) REFERENCES cases_case(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cases_case_shared_with_users cases_case_shared_with_users_user_id_291730e1_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY cases_case_shared_with_users
    ADD CONSTRAINT cases_case_shared_with_users_user_id_291730e1_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cases_case cases_case_user_id_bc4e6df6_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY cases_case
    ADD CONSTRAINT cases_case_user_id_bc4e6df6_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: diseases_gene_diseases diseases_gene_diseas_disease_id_bd05da51_fk_diseases_; Type: FK CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY diseases_gene_diseases
    ADD CONSTRAINT diseases_gene_diseas_disease_id_bd05da51_fk_diseases_ FOREIGN KEY (disease_id) REFERENCES diseases_disease(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: diseases_gene_diseases diseases_gene_diseases_gene_id_9b15fab6_fk_diseases_gene_id; Type: FK CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY diseases_gene_diseases
    ADD CONSTRAINT diseases_gene_diseases_gene_id_9b15fab6_fk_diseases_gene_id FOREIGN KEY (gene_id) REFERENCES diseases_gene(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: diseases_hgmdgene_diseases diseases_hgmdgene_di_hgmdgene_id_d9f66777_fk_diseases_; Type: FK CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY diseases_hgmdgene_diseases
    ADD CONSTRAINT diseases_hgmdgene_di_hgmdgene_id_d9f66777_fk_diseases_ FOREIGN KEY (hgmdgene_id) REFERENCES diseases_hgmdgene(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: diseases_hgmdgene_diseases diseases_hgmdgene_di_hgmdphenotype_id_c4b4eb3f_fk_diseases_; Type: FK CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY diseases_hgmdgene_diseases
    ADD CONSTRAINT diseases_hgmdgene_di_hgmdphenotype_id_c4b4eb3f_fk_diseases_ FOREIGN KEY (hgmdphenotype_id) REFERENCES diseases_hgmdphenotype(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: diseases_hgmdmutation diseases_hgmdmutatio_phenotype_id_5343ded5_fk_diseases_; Type: FK CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY diseases_hgmdmutation
    ADD CONSTRAINT diseases_hgmdmutatio_phenotype_id_5343ded5_fk_diseases_ FOREIGN KEY (phenotype_id) REFERENCES diseases_hgmdphenotype(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: diseases_hgmdmutation diseases_hgmdmutation_gene_id_4286e0ed_fk_diseases_hgmdgene_id; Type: FK CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY diseases_hgmdmutation
    ADD CONSTRAINT diseases_hgmdmutation_gene_id_4286e0ed_fk_diseases_hgmdgene_id FOREIGN KEY (gene_id) REFERENCES diseases_hgmdgene(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_content_type_id_c4bce8eb_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_user_id_c564eba6_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: djcelery_periodictask djcelery_periodictas_crontab_id_75609bab_fk_djcelery_; Type: FK CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY djcelery_periodictask
    ADD CONSTRAINT djcelery_periodictas_crontab_id_75609bab_fk_djcelery_ FOREIGN KEY (crontab_id) REFERENCES djcelery_crontabschedule(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: djcelery_periodictask djcelery_periodictas_interval_id_b426ab02_fk_djcelery_; Type: FK CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY djcelery_periodictask
    ADD CONSTRAINT djcelery_periodictas_interval_id_b426ab02_fk_djcelery_ FOREIGN KEY (interval_id) REFERENCES djcelery_intervalschedule(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: djcelery_taskstate djcelery_taskstate_worker_id_f7f57a05_fk_djcelery_; Type: FK CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY djcelery_taskstate
    ADD CONSTRAINT djcelery_taskstate_worker_id_f7f57a05_fk_djcelery_ FOREIGN KEY (worker_id) REFERENCES djcelery_workerstate(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: djkombu_message djkombu_message_queue_id_38d205a7_fk_djkombu_queue_id; Type: FK CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY djkombu_message
    ADD CONSTRAINT djkombu_message_queue_id_38d205a7_fk_djkombu_queue_id FOREIGN KEY (queue_id) REFERENCES djkombu_queue(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: genes_cgdentry_CONDITIONS genes_cgdentry_CONDI_cgdcondition_id_953c0630_fk_genes_cgd; Type: FK CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY "genes_cgdentry_CONDITIONS"
    ADD CONSTRAINT "genes_cgdentry_CONDI_cgdcondition_id_953c0630_fk_genes_cgd" FOREIGN KEY (cgdcondition_id) REFERENCES genes_cgdcondition(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: genes_cgdentry_CONDITIONS genes_cgdentry_CONDI_cgdentry_id_7c9ad17c_fk_genes_cgd; Type: FK CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY "genes_cgdentry_CONDITIONS"
    ADD CONSTRAINT "genes_cgdentry_CONDI_cgdentry_id_7c9ad17c_fk_genes_cgd" FOREIGN KEY (cgdentry_id) REFERENCES genes_cgdentry(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: genes_cgdentry_INTERVENTION_CATEGORIES genes_cgdentry_INTER_cgdentry_id_2660621e_fk_genes_cgd; Type: FK CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY "genes_cgdentry_INTERVENTION_CATEGORIES"
    ADD CONSTRAINT "genes_cgdentry_INTER_cgdentry_id_2660621e_fk_genes_cgd" FOREIGN KEY (cgdentry_id) REFERENCES genes_cgdentry(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: genes_cgdentry_INTERVENTION_CATEGORIES genes_cgdentry_INTER_intervention_id_09582a0c_fk_genes_int; Type: FK CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY "genes_cgdentry_INTERVENTION_CATEGORIES"
    ADD CONSTRAINT "genes_cgdentry_INTER_intervention_id_09582a0c_fk_genes_int" FOREIGN KEY (intervention_id) REFERENCES genes_intervention(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: genes_cgdentry_MANIFESTATION_CATEGORIES genes_cgdentry_MANIF_cgdentry_id_fec24495_fk_genes_cgd; Type: FK CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY "genes_cgdentry_MANIFESTATION_CATEGORIES"
    ADD CONSTRAINT "genes_cgdentry_MANIF_cgdentry_id_fec24495_fk_genes_cgd" FOREIGN KEY (cgdentry_id) REFERENCES genes_cgdentry(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: genes_cgdentry_MANIFESTATION_CATEGORIES genes_cgdentry_MANIF_manifestation_id_04303717_fk_genes_man; Type: FK CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY "genes_cgdentry_MANIFESTATION_CATEGORIES"
    ADD CONSTRAINT "genes_cgdentry_MANIF_manifestation_id_04303717_fk_genes_man" FOREIGN KEY (manifestation_id) REFERENCES genes_manifestation(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: genes_gene_diseases genes_gene_diseases_disease_id_58690f60_fk_diseases_disease_id; Type: FK CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY genes_gene_diseases
    ADD CONSTRAINT genes_gene_diseases_disease_id_58690f60_fk_diseases_disease_id FOREIGN KEY (disease_id) REFERENCES diseases_disease(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: genes_gene_diseases genes_gene_diseases_gene_id_4ff7115e_fk_genes_gene_id; Type: FK CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY genes_gene_diseases
    ADD CONSTRAINT genes_gene_diseases_gene_id_4ff7115e_fk_genes_gene_id FOREIGN KEY (gene_id) REFERENCES genes_gene(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: genes_genecategory_genes genes_genecategory_g_genecategory_id_b0c0cabd_fk_genes_gen; Type: FK CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY genes_genecategory_genes
    ADD CONSTRAINT genes_genecategory_g_genecategory_id_b0c0cabd_fk_genes_gen FOREIGN KEY (genecategory_id) REFERENCES genes_genecategory(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: genes_genecategory_genes genes_genecategory_genes_gene_id_bdfa6678_fk_genes_gene_id; Type: FK CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY genes_genecategory_genes
    ADD CONSTRAINT genes_genecategory_genes_gene_id_bdfa6678_fk_genes_gene_id FOREIGN KEY (gene_id) REFERENCES genes_gene(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: genes_genelist genes_genelist_user_id_eb300f6d_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY genes_genelist
    ADD CONSTRAINT genes_genelist_user_id_eb300f6d_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: genes_goterm_children genes_goterm_childre_from_goterm_id_98c9c1f0_fk_genes_got; Type: FK CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY genes_goterm_children
    ADD CONSTRAINT genes_goterm_childre_from_goterm_id_98c9c1f0_fk_genes_got FOREIGN KEY (from_goterm_id) REFERENCES genes_goterm(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: genes_goterm_children genes_goterm_children_to_goterm_id_43061461_fk_genes_goterm_id; Type: FK CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY genes_goterm_children
    ADD CONSTRAINT genes_goterm_children_to_goterm_id_43061461_fk_genes_goterm_id FOREIGN KEY (to_goterm_id) REFERENCES genes_goterm(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: genes_goterm_parents genes_goterm_parents_from_goterm_id_164ed754_fk_genes_goterm_id; Type: FK CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY genes_goterm_parents
    ADD CONSTRAINT genes_goterm_parents_from_goterm_id_164ed754_fk_genes_goterm_id FOREIGN KEY (from_goterm_id) REFERENCES genes_goterm(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: genes_goterm_parents genes_goterm_parents_to_goterm_id_d1ec2c5d_fk_genes_goterm_id; Type: FK CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY genes_goterm_parents
    ADD CONSTRAINT genes_goterm_parents_to_goterm_id_d1ec2c5d_fk_genes_goterm_id FOREIGN KEY (to_goterm_id) REFERENCES genes_goterm(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: genes_membership genes_membership_gene_id_83331c66_fk_genes_gene_id; Type: FK CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY genes_membership
    ADD CONSTRAINT genes_membership_gene_id_83331c66_fk_genes_gene_id FOREIGN KEY (gene_id) REFERENCES genes_gene(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: genes_membership genes_membership_group_id_f4b3d9ed_fk_genes_genecategory_id; Type: FK CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY genes_membership
    ADD CONSTRAINT genes_membership_group_id_f4b3d9ed_fk_genes_genecategory_id FOREIGN KEY (group_id) REFERENCES genes_genecategory(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: individuals_controlvariant individuals_controlv_controlgroup_id_6b62649d_fk_individua; Type: FK CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY individuals_controlvariant
    ADD CONSTRAINT individuals_controlv_controlgroup_id_6b62649d_fk_individua FOREIGN KEY (controlgroup_id) REFERENCES individuals_controlgroup(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: individuals_group_members individuals_group_me_group_id_ea56f429_fk_individua; Type: FK CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY individuals_group_members
    ADD CONSTRAINT individuals_group_me_group_id_ea56f429_fk_individua FOREIGN KEY (group_id) REFERENCES individuals_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: individuals_group_members individuals_group_me_individual_id_497e1be9_fk_individua; Type: FK CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY individuals_group_members
    ADD CONSTRAINT individuals_group_me_individual_id_497e1be9_fk_individua FOREIGN KEY (individual_id) REFERENCES individuals_individual(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: individuals_individual_shared_with_groups individuals_individu_individual_id_05de08af_fk_individua; Type: FK CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY individuals_individual_shared_with_groups
    ADD CONSTRAINT individuals_individu_individual_id_05de08af_fk_individua FOREIGN KEY (individual_id) REFERENCES individuals_individual(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: individuals_individual_shared_with_users individuals_individu_individual_id_47081c26_fk_individua; Type: FK CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY individuals_individual_shared_with_users
    ADD CONSTRAINT individuals_individu_individual_id_47081c26_fk_individua FOREIGN KEY (individual_id) REFERENCES individuals_individual(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: individuals_individual_shared_with_users individuals_individu_user_id_b9f3fea8_fk_auth_user; Type: FK CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY individuals_individual_shared_with_users
    ADD CONSTRAINT individuals_individu_user_id_b9f3fea8_fk_auth_user FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: individuals_individual_shared_with_groups individuals_individu_usergroup_id_e13d283c_fk_individua; Type: FK CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY individuals_individual_shared_with_groups
    ADD CONSTRAINT individuals_individu_usergroup_id_e13d283c_fk_individua FOREIGN KEY (usergroup_id) REFERENCES individuals_usergroup(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: individuals_individual individuals_individual_user_id_8e362273_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY individuals_individual
    ADD CONSTRAINT individuals_individual_user_id_8e362273_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: individuals_usergroup_members individuals_usergrou_usergroup_id_88110220_fk_individua; Type: FK CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY individuals_usergroup_members
    ADD CONSTRAINT individuals_usergrou_usergroup_id_88110220_fk_individua FOREIGN KEY (usergroup_id) REFERENCES individuals_usergroup(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: individuals_usergroup_members individuals_usergroup_members_user_id_92da6911_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY individuals_usergroup_members
    ADD CONSTRAINT individuals_usergroup_members_user_id_92da6911_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: projects_project_files projects_project_fil_project_id_1b037a58_fk_projects_; Type: FK CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY projects_project_files
    ADD CONSTRAINT projects_project_fil_project_id_1b037a58_fk_projects_ FOREIGN KEY (project_id) REFERENCES projects_project(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: projects_project_files projects_project_files_file_id_d1fa60e4_fk_files_file_id; Type: FK CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY projects_project_files
    ADD CONSTRAINT projects_project_files_file_id_d1fa60e4_fk_files_file_id FOREIGN KEY (file_id) REFERENCES files_file(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: projects_project_groups projects_project_gro_project_id_3bf040aa_fk_projects_; Type: FK CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY projects_project_groups
    ADD CONSTRAINT projects_project_gro_project_id_3bf040aa_fk_projects_ FOREIGN KEY (project_id) REFERENCES projects_project(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: projects_project_groups projects_project_groups_group_id_90ac8d97_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY projects_project_groups
    ADD CONSTRAINT projects_project_groups_group_id_90ac8d97_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: projects_project_individuals projects_project_ind_individual_id_5ca3bf25_fk_individua; Type: FK CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY projects_project_individuals
    ADD CONSTRAINT projects_project_ind_individual_id_5ca3bf25_fk_individua FOREIGN KEY (individual_id) REFERENCES individuals_individual(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: projects_project_individuals projects_project_ind_project_id_b9258353_fk_projects_; Type: FK CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY projects_project_individuals
    ADD CONSTRAINT projects_project_ind_project_id_b9258353_fk_projects_ FOREIGN KEY (project_id) REFERENCES projects_project(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: projects_project_members projects_project_mem_project_id_6a04b77b_fk_projects_; Type: FK CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY projects_project_members
    ADD CONSTRAINT projects_project_mem_project_id_6a04b77b_fk_projects_ FOREIGN KEY (project_id) REFERENCES projects_project(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: projects_project_members projects_project_members_user_id_f7cc124d_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY projects_project_members
    ADD CONSTRAINT projects_project_members_user_id_f7cc124d_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: projects_project projects_project_user_id_719f19dd_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY projects_project
    ADD CONSTRAINT projects_project_user_id_719f19dd_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: socialaccount_socialtoken socialaccount_social_account_id_951f210e_fk_socialacc; Type: FK CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY socialaccount_socialtoken
    ADD CONSTRAINT socialaccount_social_account_id_951f210e_fk_socialacc FOREIGN KEY (account_id) REFERENCES socialaccount_socialaccount(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: socialaccount_socialtoken socialaccount_social_app_id_636a42d7_fk_socialacc; Type: FK CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY socialaccount_socialtoken
    ADD CONSTRAINT socialaccount_social_app_id_636a42d7_fk_socialacc FOREIGN KEY (app_id) REFERENCES socialaccount_socialapp(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: socialaccount_socialapp_sites socialaccount_social_site_id_2579dee5_fk_django_si; Type: FK CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY socialaccount_socialapp_sites
    ADD CONSTRAINT socialaccount_social_site_id_2579dee5_fk_django_si FOREIGN KEY (site_id) REFERENCES django_site(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: socialaccount_socialapp_sites socialaccount_social_socialapp_id_97fb6e7d_fk_socialacc; Type: FK CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY socialaccount_socialapp_sites
    ADD CONSTRAINT socialaccount_social_socialapp_id_97fb6e7d_fk_socialacc FOREIGN KEY (socialapp_id) REFERENCES socialaccount_socialapp(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: socialaccount_socialaccount socialaccount_socialaccount_user_id_8146e70c_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: raony
--

ALTER TABLE ONLY socialaccount_socialaccount
    ADD CONSTRAINT socialaccount_socialaccount_user_id_8146e70c_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- PostgreSQL database dump complete
--

