--
-- PostgreSQL database dump
--

-- Dumped from database version 13.1
-- Dumped by pg_dump version 13.1

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
-- Name: admins; Type: TABLE; Schema: public; Owner: sunbaowu
--

CREATE TABLE public.admins (
    username character varying(20) NOT NULL,
    password text NOT NULL,
    first_name character varying(30) NOT NULL,
    last_name character varying(30) NOT NULL,
    email character varying(100) NOT NULL,
    "authorization" character varying(100) DEFAULT 'regular'::character varying NOT NULL,
    created timestamp with time zone DEFAULT now() NOT NULL,
    pwd_token text DEFAULT ''::text,
    is_active boolean DEFAULT true NOT NULL
);


--
-- Name: appointments; Type: TABLE; Schema: public; Owner: sunbaowu
--

CREATE TABLE public.appointments (
    id integer NOT NULL,
    event_id text DEFAULT ''::text,
    provider_username character varying(20),
    customer_username character varying(20),
    start timestamp with time zone NOT NULL,
    "end" timestamp with time zone NOT NULL,
    service_id integer,
    note text DEFAULT ''::text NOT NULL,
    updated timestamp with time zone DEFAULT now() NOT NULL,
    created timestamp with time zone DEFAULT now() NOT NULL,
    is_active boolean DEFAULT true NOT NULL
);


--
-- Name: appointments_id_seq; Type: SEQUENCE; Schema: public; Owner: sunbaowu
--

CREATE SEQUENCE public.appointments_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;



--
-- Name: appointments_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sunbaowu
--

ALTER SEQUENCE public.appointments_id_seq OWNED BY public.appointments.id;


--
-- Name: categories; Type: TABLE; Schema: public; Owner: sunbaowu
--

CREATE TABLE public.categories (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    is_active boolean DEFAULT true NOT NULL
);



--
-- Name: categories_id_seq; Type: SEQUENCE; Schema: public; Owner: sunbaowu
--

CREATE SEQUENCE public.categories_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;



--
-- Name: categories_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sunbaowu
--

ALTER SEQUENCE public.categories_id_seq OWNED BY public.categories.id;


--
-- Name: categories_services; Type: TABLE; Schema: public; Owner: sunbaowu
--

CREATE TABLE public.categories_services (
    category_id integer NOT NULL,
    service_id integer NOT NULL
);



--
-- Name: schedules; Type: TABLE; Schema: public; Owner: sunbaowu
--

CREATE TABLE public.schedules (
    username character varying(20) NOT NULL,
    date_exp character varying(20) NOT NULL,
    schedules text DEFAULT ''::text NOT NULL,
    is_active boolean DEFAULT true NOT NULL
);



--
-- Name: services; Type: TABLE; Schema: public; Owner: sunbaowu
--

CREATE TABLE public.services (
    id integer NOT NULL,
    username character varying(20),
    name character varying(100) NOT NULL,
    description text DEFAULT ''::text NOT NULL,
    image text DEFAULT ''::text,
    updated timestamp with time zone DEFAULT now() NOT NULL,
    created timestamp with time zone DEFAULT now() NOT NULL,
    is_active boolean DEFAULT true NOT NULL
);



--
-- Name: services_id_seq; Type: SEQUENCE; Schema: public; Owner: sunbaowu
--

CREATE SEQUENCE public.services_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;



--
-- Name: services_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sunbaowu
--

ALTER SEQUENCE public.services_id_seq OWNED BY public.services.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: sunbaowu
--

CREATE TABLE public.users (
    username character varying(20) NOT NULL,
    password text NOT NULL,
    first_name character varying(30) NOT NULL,
    last_name character varying(30) NOT NULL,
    email character varying(100) NOT NULL,
    phone character varying(20) DEFAULT ''::character varying,
    description text DEFAULT ''::text,
    image text DEFAULT ''::text,
    calendar_id text DEFAULT ''::text,
    calendar_email character varying(50) DEFAULT ''::character varying,
    is_provider boolean DEFAULT false NOT NULL,
    updated timestamp with time zone DEFAULT now() NOT NULL,
    created timestamp with time zone DEFAULT now() NOT NULL,
    pwd_token text DEFAULT ''::text,
    is_active boolean DEFAULT true NOT NULL
);


ALTER TABLE ONLY public.appointments ALTER COLUMN id SET DEFAULT nextval('public.appointments_id_seq'::regclass);


--
-- Name: categories id; Type: DEFAULT; Schema: public; Owner: sunbaowu
--

ALTER TABLE ONLY public.categories ALTER COLUMN id SET DEFAULT nextval('public.categories_id_seq'::regclass);


--
-- Name: services id; Type: DEFAULT; Schema: public; Owner: sunbaowu
--

ALTER TABLE ONLY public.services ALTER COLUMN id SET DEFAULT nextval('public.services_id_seq'::regclass);


--
-- Data for Name: admins; Type: TABLE DATA; Schema: public; Owner: sunbaowu
--

COPY public.admins (username, password, first_name, last_name, email, "authorization", created, pwd_token, is_active) FROM stdin;
admin	$2b$12$10r0lOYK2mqxFYmn0Pus.eCVFQv.jQytsRehGYPqeFSd/kPe11OJW	admin	admin	bobowu@outlook.com	administrator	2021-03-22 07:22:46.690041-04		t
admin_test	$2b$12$VpyL2TPDIbdefnXUPgShnePKJEhYiZ9I.mCbuzh.aFwGhSYTVos5e	admin_test	admin_test	ybdevs.com@gmail.com	regular	2021-03-22 07:22:47.043866-04		t
\.


--
-- Data for Name: appointments; Type: TABLE DATA; Schema: public; Owner: sunbaowu
--

COPY public.appointments (id, event_id, provider_username, customer_username, start, "end", service_id, note, updated, created, is_active) FROM stdin;
1		crazylion587	brownelephant861	2021-03-22 09:00:00-04	2021-03-22 10:00:00-04	50		2021-03-22 07:24:30.96103-04	2021-03-22 07:24:30.96103-04	t
\.


--
-- Data for Name: categories; Type: TABLE DATA; Schema: public; Owner: sunbaowu
--

COPY public.categories (id, name, is_active) FROM stdin;
1	Finance	t
2	Accounting	t
3	Taxes	t
4	Investment	t
5	Auto Insurance	t
6	Home Insurance	t
7	Life Insurance	t
\.


--
-- Data for Name: categories_services; Type: TABLE DATA; Schema: public; Owner: sunbaowu
--

COPY public.categories_services (category_id, service_id) FROM stdin;
6	1
2	2
2	3
2	4
1	5
1	6
2	7
7	8
6	9
7	10
4	11
4	12
3	13
5	14
6	15
6	16
5	17
2	18
3	19
6	20
7	21
3	22
3	23
2	24
4	25
6	26
5	27
5	28
3	29
4	30
7	31
5	32
7	33
7	34
6	35
1	36
7	37
2	38
5	39
1	40
4	41
7	42
2	43
6	44
5	45
6	46
2	47
7	48
2	49
5	50
\.


--
-- Data for Name: schedules; Type: TABLE DATA; Schema: public; Owner: sunbaowu
--

COPY public.schedules (username, date_exp, schedules, is_active) FROM stdin;
crazyelephant470	1	[{"start": "09:00", "end": "10:00"} , {"start": "11:00", "end": "12:00"}]	t
crazyelephant470	2	[{"start": "13:00", "end": "14:00"} , {"start": "14:00", "end": "15:00"}]	t
crazyelephant470	5	[{"start": "10:00", "end": "12:00"} , {"start": "15:00", "end": "16:00"}]	t
silverwolf580	0	[{"start": "09:00", "end": "10:00"} , {"start": "11:00", "end": "12:00"}]	t
silverwolf580	3	[{"start": "13:00", "end": "14:00"} , {"start": "14:00", "end": "15:00"}]	t
silverwolf580	6	[{"start": "10:00", "end": "12:00"} , {"start": "15:00", "end": "16:00"}]	t
blackfrog937	0	[{"start": "09:00", "end": "10:00"} , {"start": "11:00", "end": "12:00"}]	t
blackfrog937	2	[{"start": "13:00", "end": "14:00"} , {"start": "14:00", "end": "15:00"}]	t
blackfrog937	5	[{"start": "10:00", "end": "12:00"} , {"start": "15:00", "end": "16:00"}]	t
lazylion973	1	[{"start": "09:00", "end": "10:00"} , {"start": "11:00", "end": "12:00"}]	t
lazylion973	3	[{"start": "13:00", "end": "14:00"} , {"start": "14:00", "end": "15:00"}]	t
lazylion973	5	[{"start": "10:00", "end": "12:00"} , {"start": "15:00", "end": "16:00"}]	t
bluebutterfly264	0	[{"start": "09:00", "end": "10:00"} , {"start": "11:00", "end": "12:00"}]	t
bluebutterfly264	2	[{"start": "13:00", "end": "14:00"} , {"start": "14:00", "end": "15:00"}]	t
bluebutterfly264	5	[{"start": "10:00", "end": "12:00"} , {"start": "15:00", "end": "16:00"}]	t
bigmouse962	1	[{"start": "09:00", "end": "10:00"} , {"start": "11:00", "end": "12:00"}]	t
bigmouse962	2	[{"start": "13:00", "end": "14:00"} , {"start": "14:00", "end": "15:00"}]	t
bigmouse962	5	[{"start": "10:00", "end": "12:00"} , {"start": "15:00", "end": "16:00"}]	t
organicfish120	1	[{"start": "09:00", "end": "10:00"} , {"start": "11:00", "end": "12:00"}]	t
organicfish120	2	[{"start": "13:00", "end": "14:00"} , {"start": "14:00", "end": "15:00"}]	t
organicfish120	4	[{"start": "10:00", "end": "12:00"} , {"start": "15:00", "end": "16:00"}]	t
bigrabbit114	0	[{"start": "09:00", "end": "10:00"} , {"start": "11:00", "end": "12:00"}]	t
bigrabbit114	3	[{"start": "13:00", "end": "14:00"} , {"start": "14:00", "end": "15:00"}]	t
bigrabbit114	6	[{"start": "10:00", "end": "12:00"} , {"start": "15:00", "end": "16:00"}]	t
sadlion440	1	[{"start": "09:00", "end": "10:00"} , {"start": "11:00", "end": "12:00"}]	t
sadlion440	3	[{"start": "13:00", "end": "14:00"} , {"start": "14:00", "end": "15:00"}]	t
sadlion440	4	[{"start": "10:00", "end": "12:00"} , {"start": "15:00", "end": "16:00"}]	t
lazypeacock493	1	[{"start": "09:00", "end": "10:00"} , {"start": "11:00", "end": "12:00"}]	t
lazypeacock493	3	[{"start": "13:00", "end": "14:00"} , {"start": "14:00", "end": "15:00"}]	t
lazypeacock493	6	[{"start": "10:00", "end": "12:00"} , {"start": "15:00", "end": "16:00"}]	t
bigcat818	1	[{"start": "09:00", "end": "10:00"} , {"start": "11:00", "end": "12:00"}]	t
bigcat818	3	[{"start": "13:00", "end": "14:00"} , {"start": "14:00", "end": "15:00"}]	t
bigcat818	4	[{"start": "10:00", "end": "12:00"} , {"start": "15:00", "end": "16:00"}]	t
silverduck953	0	[{"start": "09:00", "end": "10:00"} , {"start": "11:00", "end": "12:00"}]	t
silverduck953	2	[{"start": "13:00", "end": "14:00"} , {"start": "14:00", "end": "15:00"}]	t
silverduck953	5	[{"start": "10:00", "end": "12:00"} , {"start": "15:00", "end": "16:00"}]	t
whitekoala828	1	[{"start": "09:00", "end": "10:00"} , {"start": "11:00", "end": "12:00"}]	t
whitekoala828	2	[{"start": "13:00", "end": "14:00"} , {"start": "14:00", "end": "15:00"}]	t
whitekoala828	6	[{"start": "10:00", "end": "12:00"} , {"start": "15:00", "end": "16:00"}]	t
whiteduck570	1	[{"start": "09:00", "end": "10:00"} , {"start": "11:00", "end": "12:00"}]	t
whiteduck570	2	[{"start": "13:00", "end": "14:00"} , {"start": "14:00", "end": "15:00"}]	t
whiteduck570	4	[{"start": "10:00", "end": "12:00"} , {"start": "15:00", "end": "16:00"}]	t
yellowostrich706	0	[{"start": "09:00", "end": "10:00"} , {"start": "11:00", "end": "12:00"}]	t
yellowostrich706	2	[{"start": "13:00", "end": "14:00"} , {"start": "14:00", "end": "15:00"}]	t
yellowostrich706	4	[{"start": "10:00", "end": "12:00"} , {"start": "15:00", "end": "16:00"}]	t
crazylion587	1	[{"start": "09:00", "end": "10:00"} , {"start": "11:00", "end": "12:00"}]	t
crazylion587	2	[{"start": "13:00", "end": "14:00"} , {"start": "14:00", "end": "15:00"}]	t
crazylion587	5	[{"start": "10:00", "end": "12:00"} , {"start": "15:00", "end": "16:00"}]	t
purplebird449	1	[{"start": "09:00", "end": "10:00"} , {"start": "11:00", "end": "12:00"}]	t
purplebird449	2	[{"start": "13:00", "end": "14:00"} , {"start": "14:00", "end": "15:00"}]	t
purplebird449	6	[{"start": "10:00", "end": "12:00"} , {"start": "15:00", "end": "16:00"}]	t
heavypanda785	1	[{"start": "09:00", "end": "10:00"} , {"start": "11:00", "end": "12:00"}]	t
heavypanda785	3	[{"start": "13:00", "end": "14:00"} , {"start": "14:00", "end": "15:00"}]	t
heavypanda785	4	[{"start": "10:00", "end": "12:00"} , {"start": "15:00", "end": "16:00"}]	t
browngorilla178	0	[{"start": "09:00", "end": "10:00"} , {"start": "11:00", "end": "12:00"}]	t
browngorilla178	2	[{"start": "13:00", "end": "14:00"} , {"start": "14:00", "end": "15:00"}]	t
browngorilla178	6	[{"start": "10:00", "end": "12:00"} , {"start": "15:00", "end": "16:00"}]	t
goldenbutterfly683	0	[{"start": "09:00", "end": "10:00"} , {"start": "11:00", "end": "12:00"}]	t
goldenbutterfly683	2	[{"start": "13:00", "end": "14:00"} , {"start": "14:00", "end": "15:00"}]	t
goldenbutterfly683	4	[{"start": "10:00", "end": "12:00"} , {"start": "15:00", "end": "16:00"}]	t
bigpanda663	0	[{"start": "09:00", "end": "10:00"} , {"start": "11:00", "end": "12:00"}]	t
bigpanda663	2	[{"start": "13:00", "end": "14:00"} , {"start": "14:00", "end": "15:00"}]	t
bigpanda663	5	[{"start": "10:00", "end": "12:00"} , {"start": "15:00", "end": "16:00"}]	t
organicbird867	0	[{"start": "09:00", "end": "10:00"} , {"start": "11:00", "end": "12:00"}]	t
organicbird867	2	[{"start": "13:00", "end": "14:00"} , {"start": "14:00", "end": "15:00"}]	t
organicbird867	6	[{"start": "10:00", "end": "12:00"} , {"start": "15:00", "end": "16:00"}]	t
blackelephant183	0	[{"start": "09:00", "end": "10:00"} , {"start": "11:00", "end": "12:00"}]	t
blackelephant183	2	[{"start": "13:00", "end": "14:00"} , {"start": "14:00", "end": "15:00"}]	t
blackelephant183	4	[{"start": "10:00", "end": "12:00"} , {"start": "15:00", "end": "16:00"}]	t
bluedog478	0	[{"start": "09:00", "end": "10:00"} , {"start": "11:00", "end": "12:00"}]	t
bluedog478	3	[{"start": "13:00", "end": "14:00"} , {"start": "14:00", "end": "15:00"}]	t
bluedog478	4	[{"start": "10:00", "end": "12:00"} , {"start": "15:00", "end": "16:00"}]	t
tinypanda585	0	[{"start": "09:00", "end": "10:00"} , {"start": "11:00", "end": "12:00"}]	t
tinypanda585	3	[{"start": "13:00", "end": "14:00"} , {"start": "14:00", "end": "15:00"}]	t
tinypanda585	5	[{"start": "10:00", "end": "12:00"} , {"start": "15:00", "end": "16:00"}]	t
heavyladybug748	1	[{"start": "09:00", "end": "10:00"} , {"start": "11:00", "end": "12:00"}]	t
heavyladybug748	3	[{"start": "13:00", "end": "14:00"} , {"start": "14:00", "end": "15:00"}]	t
heavyladybug748	4	[{"start": "10:00", "end": "12:00"} , {"start": "15:00", "end": "16:00"}]	t
greenlion478	0	[{"start": "09:00", "end": "10:00"} , {"start": "11:00", "end": "12:00"}]	t
greenlion478	3	[{"start": "13:00", "end": "14:00"} , {"start": "14:00", "end": "15:00"}]	t
greenlion478	6	[{"start": "10:00", "end": "12:00"} , {"start": "15:00", "end": "16:00"}]	t
blackgorilla620	0	[{"start": "09:00", "end": "10:00"} , {"start": "11:00", "end": "12:00"}]	t
blackgorilla620	2	[{"start": "13:00", "end": "14:00"} , {"start": "14:00", "end": "15:00"}]	t
blackgorilla620	5	[{"start": "10:00", "end": "12:00"} , {"start": "15:00", "end": "16:00"}]	t
smallkoala709	1	[{"start": "09:00", "end": "10:00"} , {"start": "11:00", "end": "12:00"}]	t
smallkoala709	2	[{"start": "13:00", "end": "14:00"} , {"start": "14:00", "end": "15:00"}]	t
smallkoala709	4	[{"start": "10:00", "end": "12:00"} , {"start": "15:00", "end": "16:00"}]	t
goldenladybug179	1	[{"start": "09:00", "end": "10:00"} , {"start": "11:00", "end": "12:00"}]	t
goldenladybug179	3	[{"start": "13:00", "end": "14:00"} , {"start": "14:00", "end": "15:00"}]	t
goldenladybug179	4	[{"start": "10:00", "end": "12:00"} , {"start": "15:00", "end": "16:00"}]	t
\.


--
-- Data for Name: services; Type: TABLE DATA; Schema: public; Owner: sunbaowu
--

COPY public.services (id, username, name, description, image, updated, created, is_active) FROM stdin;
1	goldenbutterfly683	Molina's Home Insurance Service	Professional Home Insurance Service from Eugenia Molina		2021-03-22 07:23:16.066657-04	2021-03-22 07:23:16.066657-04	t
2	bigrabbit114	Nybakken's Accounting Service	Professional Accounting Service from Aksel Nybakken		2021-03-22 07:23:16.123485-04	2021-03-22 07:23:16.123485-04	t
3	bigcat818	Gaustad's Accounting Service	Professional Accounting Service from Mio Gaustad		2021-03-22 07:23:16.1434-04	2021-03-22 07:23:16.1434-04	t
4	bigrabbit114	Nybakken's Accounting Service	Professional Accounting Service from Aksel Nybakken		2021-03-22 07:23:16.173475-04	2021-03-22 07:23:16.173475-04	t
5	purplebird449	Perala's Finance Service	Professional Finance Service from Pinja Perala		2021-03-22 07:23:16.210372-04	2021-03-22 07:23:16.210372-04	t
6	lazypeacock493	Romero's Finance Service	Professional Finance Service from Vanesa Romero		2021-03-22 07:23:16.24876-04	2021-03-22 07:23:16.24876-04	t
7	silverduck953	Warren's Accounting Service	Professional Accounting Service from Patricia Warren		2021-03-22 07:23:16.28438-04	2021-03-22 07:23:16.28438-04	t
8	yellowostrich706	Ilıcalı's Life Insurance Service	Professional Life Insurance Service from Elif Ilıcalı		2021-03-22 07:23:16.324986-04	2021-03-22 07:23:16.324986-04	t
9	bigcat818	Gaustad's Home Insurance Service	Professional Home Insurance Service from Mio Gaustad		2021-03-22 07:23:16.370966-04	2021-03-22 07:23:16.370966-04	t
10	heavypanda785	West's Life Insurance Service	Professional Life Insurance Service from Josh West		2021-03-22 07:23:16.410981-04	2021-03-22 07:23:16.410981-04	t
11	sadlion440	Larsen's Investment Service	Professional Investment Service from Nicoline Larsen		2021-03-22 07:23:16.440383-04	2021-03-22 07:23:16.440383-04	t
12	bluebutterfly264	Hokkanen's Investment Service	Professional Investment Service from Iiris Hokkanen		2021-03-22 07:23:16.48469-04	2021-03-22 07:23:16.48469-04	t
13	goldenbutterfly683	Molina's Taxes Service	Professional Taxes Service from Eugenia Molina		2021-03-22 07:23:16.539955-04	2021-03-22 07:23:16.539955-04	t
14	blackfrog937	Olson's Auto Insurance Service	Professional Auto Insurance Service from Mandy Olson		2021-03-22 07:23:16.566429-04	2021-03-22 07:23:16.566429-04	t
15	browngorilla178	گلشن's Home Insurance Service	Professional Home Insurance Service from غزل گلشن		2021-03-22 07:23:16.592453-04	2021-03-22 07:23:16.592453-04	t
16	sadlion440	Larsen's Home Insurance Service	Professional Home Insurance Service from Nicoline Larsen		2021-03-22 07:23:16.622256-04	2021-03-22 07:23:16.622256-04	t
17	whitekoala828	Farias's Auto Insurance Service	Professional Auto Insurance Service from Toledo Farias		2021-03-22 07:23:16.647288-04	2021-03-22 07:23:16.647288-04	t
18	sadlion440	Larsen's Accounting Service	Professional Accounting Service from Nicoline Larsen		2021-03-22 07:23:16.675179-04	2021-03-22 07:23:16.675179-04	t
19	silverduck953	Warren's Taxes Service	Professional Taxes Service from Patricia Warren		2021-03-22 07:23:16.704636-04	2021-03-22 07:23:16.704636-04	t
20	crazyelephant470	Sæterbø's Home Insurance Service	Professional Home Insurance Service from Cassandra Sæterbø		2021-03-22 07:23:16.72695-04	2021-03-22 07:23:16.72695-04	t
21	organicfish120	Brown's Life Insurance Service	Professional Life Insurance Service from John Brown		2021-03-22 07:23:16.754011-04	2021-03-22 07:23:16.754011-04	t
22	silverduck953	Warren's Taxes Service	Professional Taxes Service from Patricia Warren		2021-03-22 07:23:16.78232-04	2021-03-22 07:23:16.78232-04	t
23	bluebutterfly264	Hokkanen's Taxes Service	Professional Taxes Service from Iiris Hokkanen		2021-03-22 07:23:16.809619-04	2021-03-22 07:23:16.809619-04	t
24	sadlion440	Larsen's Accounting Service	Professional Accounting Service from Nicoline Larsen		2021-03-22 07:23:16.841625-04	2021-03-22 07:23:16.841625-04	t
25	sadlion440	Larsen's Investment Service	Professional Investment Service from Nicoline Larsen		2021-03-22 07:23:16.873646-04	2021-03-22 07:23:16.873646-04	t
26	whiteduck570	Otte's Home Insurance Service	Professional Home Insurance Service from Hans-Günther Otte		2021-03-22 07:23:16.908983-04	2021-03-22 07:23:16.908983-04	t
27	yellowostrich706	Ilıcalı's Auto Insurance Service	Professional Auto Insurance Service from Elif Ilıcalı		2021-03-22 07:23:16.942675-04	2021-03-22 07:23:16.942675-04	t
28	lazypeacock493	Romero's Auto Insurance Service	Professional Auto Insurance Service from Vanesa Romero		2021-03-22 07:23:16.974634-04	2021-03-22 07:23:16.974634-04	t
29	whitekoala828	Farias's Taxes Service	Professional Taxes Service from Toledo Farias		2021-03-22 07:23:17.003853-04	2021-03-22 07:23:17.003853-04	t
30	lazylion973	Laurent's Investment Service	Professional Investment Service from Tim Laurent		2021-03-22 07:23:17.027154-04	2021-03-22 07:23:17.027154-04	t
31	silverduck953	Warren's Life Insurance Service	Professional Life Insurance Service from Patricia Warren		2021-03-22 07:23:17.058587-04	2021-03-22 07:23:17.058587-04	t
32	bigcat818	Gaustad's Auto Insurance Service	Professional Auto Insurance Service from Mio Gaustad		2021-03-22 07:23:17.091805-04	2021-03-22 07:23:17.091805-04	t
33	heavypanda785	West's Life Insurance Service	Professional Life Insurance Service from Josh West		2021-03-22 07:23:17.12484-04	2021-03-22 07:23:17.12484-04	t
34	bluebutterfly264	Hokkanen's Life Insurance Service	Professional Life Insurance Service from Iiris Hokkanen		2021-03-22 07:23:17.158367-04	2021-03-22 07:23:17.158367-04	t
35	yellowostrich706	Ilıcalı's Home Insurance Service	Professional Home Insurance Service from Elif Ilıcalı		2021-03-22 07:23:17.192211-04	2021-03-22 07:23:17.192211-04	t
36	browngorilla178	گلشن's Finance Service	Professional Finance Service from غزل گلشن		2021-03-22 07:23:17.226445-04	2021-03-22 07:23:17.226445-04	t
37	whiteduck570	Otte's Life Insurance Service	Professional Life Insurance Service from Hans-Günther Otte		2021-03-22 07:23:17.258113-04	2021-03-22 07:23:17.258113-04	t
38	crazylion587	Pires's Accounting Service	Professional Accounting Service from Castelino Pires		2021-03-22 07:23:17.29196-04	2021-03-22 07:23:17.29196-04	t
39	lazypeacock493	Romero's Auto Insurance Service	Professional Auto Insurance Service from Vanesa Romero		2021-03-22 07:23:17.3272-04	2021-03-22 07:23:17.3272-04	t
40	bigmouse962	Velasco's Finance Service	Professional Finance Service from Beatriz Velasco		2021-03-22 07:23:17.358107-04	2021-03-22 07:23:17.358107-04	t
41	crazylion587	Pires's Investment Service	Professional Investment Service from Castelino Pires		2021-03-22 07:23:17.388092-04	2021-03-22 07:23:17.388092-04	t
42	yellowostrich706	Ilıcalı's Life Insurance Service	Professional Life Insurance Service from Elif Ilıcalı		2021-03-22 07:23:17.416513-04	2021-03-22 07:23:17.416513-04	t
43	whiteduck570	Otte's Accounting Service	Professional Accounting Service from Hans-Günther Otte		2021-03-22 07:23:17.443645-04	2021-03-22 07:23:17.443645-04	t
44	browngorilla178	گلشن's Home Insurance Service	Professional Home Insurance Service from غزل گلشن		2021-03-22 07:23:17.473007-04	2021-03-22 07:23:17.473007-04	t
45	bigmouse962	Velasco's Auto Insurance Service	Professional Auto Insurance Service from Beatriz Velasco		2021-03-22 07:23:17.509202-04	2021-03-22 07:23:17.509202-04	t
46	whitekoala828	Farias's Home Insurance Service	Professional Home Insurance Service from Toledo Farias		2021-03-22 07:23:17.542995-04	2021-03-22 07:23:17.542995-04	t
47	purplebird449	Perala's Accounting Service	Professional Accounting Service from Pinja Perala		2021-03-22 07:23:17.571993-04	2021-03-22 07:23:17.571993-04	t
48	browngorilla178	گلشن's Life Insurance Service	Professional Life Insurance Service from غزل گلشن		2021-03-22 07:23:17.599623-04	2021-03-22 07:23:17.599623-04	t
49	lazylion973	Laurent's Accounting Service	Professional Accounting Service from Tim Laurent		2021-03-22 07:23:17.62621-04	2021-03-22 07:23:17.62621-04	t
50	crazylion587	Pires's Auto Insurance Service	Professional Auto Insurance Service from Castelino Pires		2021-03-22 07:23:17.656206-04	2021-03-22 07:23:17.656206-04	t
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: sunbaowu
--

COPY public.users (username, password, first_name, last_name, email, phone, description, image, calendar_id, calendar_email, is_provider, updated, created, pwd_token, is_active) FROM stdin;
brownelephant861	$2b$12$QaGeHYTmz4v/9HEUF5awN.4S4gx7UVc1Y0QzNMnr.oABZTnYH5V8m	Troy	Craig	troy.craig@example.com	8868878888					f	2021-03-22 07:23:04.911815-04	2021-03-22 07:23:04.911815-04		t
brownpeacock251	$2b$12$MX.Q98xgx.bzAAqT.fDY3.yNcae43ytNY3d3Tg7SF0CJ1C2v8AR/y	Joel	Pierce	joel.pierce@example.com	8868878888					f	2021-03-22 07:23:04.917799-04	2021-03-22 07:23:04.917799-04		t
whitedog236	$2b$12$/AIOGgno6ilaeq/6Zd2x.uSz.VM6G3XYqiJwaNm8ExVPwAezf.C5y	Stacey	Jennings	stacey.jennings@example.com	8868878888					f	2021-03-22 07:23:04.923396-04	2021-03-22 07:23:04.923396-04		t
smallelephant619	$2b$12$oArk5ehi94oS3hPscbloWOOAzClLEgP/AmM9FYHRN0G//KocGp8j.	Jack	Robinson	jack.robinson@example.com	8868878888					f	2021-03-22 07:23:04.928027-04	2021-03-22 07:23:04.928027-04		t
greenleopard875	$2b$12$K2SLbS4..pfb1sPY6kEZpOcMbcVhGmsafKW.C/Z.cm77NgkZsQpnm	Thomas	Baker	thomas.baker@example.com	8868878888					f	2021-03-22 07:23:04.932327-04	2021-03-22 07:23:04.932327-04		t
bigkoala379	$2b$12$WvpHgfRhL406a/tAuis3iOGhRfC9Qzx0b/4pGPmHB5nr6D3mHCpUS	Alice	Hughes	alice.hughes@example.com	8868878888					f	2021-03-22 07:23:04.936386-04	2021-03-22 07:23:04.936386-04		t
brownmouse274	$2b$12$QZAag0UJNz7dk9fpT8fTzO3VSD4VtObkUusnSRJ3j6iX7EaIdAkqK	Ahmet	Yeşilkaya	ahmet.yesilkaya@example.com	8868878888					f	2021-03-22 07:23:04.945583-04	2021-03-22 07:23:04.945583-04		t
yellowpeacock952	$2b$12$9..sGSbfBxH2EqwX9jkzGuDXbH842Vw/zpCwfVmrZrgisy7Tuolwm	Wilco	Van Ingen	wilco.vaningen@example.com	8868878888					f	2021-03-22 07:23:04.950829-04	2021-03-22 07:23:04.950829-04		t
angryfish246	$2b$12$6cMo.0s5WwyNG/NNRiI8WOrlOdHqPMc/ZQFSMb0PjFvsI621Z8YIy	John	Hayes	john.hayes@example.com	8868878888					f	2021-03-22 07:23:04.955719-04	2021-03-22 07:23:04.955719-04		t
bluezebra421	$2b$12$ZY3U86KRUbH4Tkm6JrHsduHPNE211Kv6zd1y75MerjeFO3ezR5yVa	آرمین	نكو نظر	armyn.nkwnzr@example.com	8868878888					f	2021-03-22 07:23:04.964129-04	2021-03-22 07:23:04.964129-04		t
beautifulsnake682	$2b$12$CewZsxU7cqbjMO6e4L/KdO/.xtSNXqpqsgI.rPirBCXzgPxIMQbsK	رونیکا	كامياران	rwnykh.kmyrn@example.com	8868878888					f	2021-03-22 07:23:04.970059-04	2021-03-22 07:23:04.970059-04		t
brownmeercat634	$2b$12$jiFjCYWXIwOj0egdAMUfq.zx5WnGMVpYGLyyMcRaSlhZg./zgU.Ru	Giray	Karaer	giray.karaer@example.com	8868878888					f	2021-03-22 07:23:04.974965-04	2021-03-22 07:23:04.974965-04		t
tinyduck747	$2b$12$kLdlAzbw1nNgVYQzTokL5uaZ9STdCYn9uyI74GdQn.3.1TvCN97Xe	Benjamin	Clement	benjamin.clement@example.com	8868878888					f	2021-03-22 07:23:04.983557-04	2021-03-22 07:23:04.983557-04		t
blueostrich564	$2b$12$Zeuu3fpyEmRuSlWSxf8uAewpOhyhnFkwdUgkTCfjmuW/iM7fd1d6C	Raihana	Pons	raihana.pons@example.com	8868878888					f	2021-03-22 07:23:04.988919-04	2021-03-22 07:23:04.988919-04		t
blueostrich591	$2b$12$W9ugaGjCNnbbW1PpbeCizOXJ6sC7wLViAb6Mx04W3ZFZEFTSCVwXK	Ilona	Hokkanen	ilona.hokkanen@example.com	8868878888					f	2021-03-22 07:23:04.998961-04	2021-03-22 07:23:04.998961-04		t
sadbird724	$2b$12$xOg1j6acvVkYygO.XnPaV.OeXEmepXNlaMxS8KwnlJ8pns6vkAjVi	Lærke	Christiansen	laerke.christiansen@example.com	8868878888					f	2021-03-22 07:23:05.004582-04	2021-03-22 07:23:05.004582-04		t
smallswan433	$2b$12$sctkZwfYDtfeEsxDROHQ1exL4IVzyOzbYzunBMVlwrPG0XkxFwjc2	Beau	Robinson	beau.robinson@example.com	8868878888					f	2021-03-22 07:23:05.008885-04	2021-03-22 07:23:05.008885-04		t
goldensnake848	$2b$12$WAhM1dNsljMZY7DAIh7bne0nhnDpg1HAeZxks3HvyuzuIMHBp5lle	Otacília	Oliveira	otacilia.oliveira@example.com	8868878888					f	2021-03-22 07:23:05.016375-04	2021-03-22 07:23:05.016375-04		t
reddog492	$2b$12$.lbhgQBco6k6PsHfdTvXKuC7vuc8Gp5R.xm7KfXfcQ4D0sLjDpzyS	Márcia	das Neves	marcia.dasneves@example.com	8868878888					f	2021-03-22 07:23:05.022527-04	2021-03-22 07:23:05.022527-04		t
organicwolf244	$2b$12$HNLAn59B0zqd8sx.QqhH/eE5tog9O2udWka8fxVdUBZMbWdqOTjmG	Lisa	Foster	lisa.foster@example.com	8868878888					f	2021-03-22 07:23:05.026804-04	2021-03-22 07:23:05.026804-04		t
orangeostrich144	$2b$12$TRv0bZrlRIMl5q9D4ATqQeaYKiOAK5U.6rGuXppo3OS3pPtD.f9vu	Katie	Miles	katie.miles@example.com	8868878888					f	2021-03-22 07:23:05.03548-04	2021-03-22 07:23:05.03548-04		t
crazydog121	$2b$12$AmJyPnVdxuFXJG/gABxFZOHAsPV2lAvwnkn7Dmc.KH8rI3qNEEJJu	Graziella	Leroux	graziella.leroux@example.com	8868878888					f	2021-03-22 07:23:05.042993-04	2021-03-22 07:23:05.042993-04		t
smallleopard481	$2b$12$TGO.hRmKcEjqX5gWi/zFuOWH6sLzma5Ohy9A4nankELhqgJocgSPy	Raul	Fuentes	raul.fuentes@example.com	8868878888					f	2021-03-22 07:23:05.057696-04	2021-03-22 07:23:05.057696-04		t
orangeladybug197	$2b$12$ybpqW.tJXaKS4QEUKbn44.lZ6bSPf73rStSZEM.QpqCLQgC0bKT8q	Asif	Bor	asif.bor@example.com	8868878888					f	2021-03-22 07:23:05.063163-04	2021-03-22 07:23:05.063163-04		t
brownbear576	$2b$12$e4ylTGnu.Byrbm28uJauXuTYiXqOtNeJooYL.RtRFmUqCXCR9Ex7q	Katie	Edwards	katie.edwards@example.com	8868878888					f	2021-03-22 07:23:05.067065-04	2021-03-22 07:23:05.067065-04		t
blackostrich565	$2b$12$IWNLoNyim087PPzVKWqteuePw788x.Zw8lkGMPE2.8NDCd3QYkivq	Luisa	Verburg	luisa.verburg@example.com	8868878888					f	2021-03-22 07:23:05.075945-04	2021-03-22 07:23:05.075945-04		t
whiteostrich592	$2b$12$TQVzhvPFaXRUqRx5uWq72eUE7rgLRrVmbBEgQcGLwhyV6Qpyxt0aq	Hansjörg	Flügge	hansjorg.flugge@example.com	8868878888					f	2021-03-22 07:23:05.084345-04	2021-03-22 07:23:05.084345-04		t
smallbird978	$2b$12$2I8tRFgJ9pULMgfTjW.5q.C9eZ/pBR5VJxscOYr4/0lPug5w5/zg6	Marion	Blanc	marion.blanc@example.com	8868878888					f	2021-03-22 07:23:05.089852-04	2021-03-22 07:23:05.089852-04		t
beautifulgoose611	$2b$12$hSATIbB5lCchMTct8wy8Iu3oGUhSpY7YqQ0WCQ9WVQ3rLGzl//SYu	Tugce	Beishuizen	tugce.beishuizen@example.com	8868878888					f	2021-03-22 07:23:05.101603-04	2021-03-22 07:23:05.101603-04		t
heavyelephant469	$2b$12$73gol98vK0IDHnM99R0hi.2aH1OFKsm0AmNs/0QcmlBmBtu4dfkZS	Perry	Dunn	perry.dunn@example.com	8868878888					f	2021-03-22 07:23:05.107362-04	2021-03-22 07:23:05.107362-04		t
yellowduck996	$2b$12$Ck64/Vmsqchoqno/x17S.umQrlaqa5FJXh.2hu/W56SzUJv0/r9pq	Layla	Hughes	layla.hughes@example.com	8868878888					f	2021-03-22 07:23:05.110957-04	2021-03-22 07:23:05.110957-04		t
silvermouse487	$2b$12$sBs..Xprs/yWq49fROly.uenW0phZ5kMCo.jUQAWTDXKgBYEeKxzC	Emilia	Kauppila	emilia.kauppila@example.com	8868878888					f	2021-03-22 07:23:05.117891-04	2021-03-22 07:23:05.117891-04		t
happypanda994	$2b$12$/3Q7d6ZN9h/20z6kBQJvY.8nJ4f2wCYJ0egDSOmivxbELvwyMq3ii	Emma	Mitchell	emma.mitchell@example.com	8868878888					f	2021-03-22 07:23:05.124226-04	2021-03-22 07:23:05.124226-04		t
angrybear964	$2b$12$OhyGm0vakE0ywSyiU0voLe0HMqOhNDuV1J2cM43WLDjRKkplcBc8O	Suzanne	Bailey	suzanne.bailey@example.com	8868878888					f	2021-03-22 07:23:05.135119-04	2021-03-22 07:23:05.135119-04		t
brownzebra125	$2b$12$nz9ygp2CosUm5dFxxRKKkOwW48c5RYl6DhtjU0pEZJ9Tl.UJwj9RK	Cengiz	Tacke	cengiz.tacke@example.com	8868878888					f	2021-03-22 07:23:05.14114-04	2021-03-22 07:23:05.14114-04		t
heavypeacock656	$2b$12$RT3PVVuEzSNxUfqCQCPjHeNJVyMBxecN.cmPO80ZBxuLAqBkGu4ca	Kathryn	Rivera	kathryn.rivera@example.com	8868878888					f	2021-03-22 07:23:05.151097-04	2021-03-22 07:23:05.151097-04		t
silverleopard639	$2b$12$OW5T7oZCgCaQRYJ94h0WOetqGXSBwZRabUto2nADjgD0jSQe3o6gm	Ricky	Fleming	ricky.fleming@example.com	8868878888					f	2021-03-22 07:23:05.156659-04	2021-03-22 07:23:05.156659-04		t
silverbird210	$2b$12$p.z4soXz9AHNekogssuJJOB0h31bX5r6v1r5Gwew6PssKHjgNNtRa	Arlene	Allen	arlene.allen@example.com	8868878888					f	2021-03-22 07:23:05.168884-04	2021-03-22 07:23:05.168884-04		t
lazyleopard877	$2b$12$ih0l6vvC4.qx6SGmnWQMS.ERclJ0qus2vnO9F3NSFkx4fF2zJjwfy	Alex	Rempel	alex.rempel@example.com	8868878888					f	2021-03-22 07:23:05.175597-04	2021-03-22 07:23:05.175597-04		t
goldenbear227	$2b$12$LVvMbC8qhRefoivbkaxVa.EzsvJdNJFJjBneYAu4o9cTxAq7WtMUy	Mikkel	Nielsen	mikkel.nielsen@example.com	8868878888					f	2021-03-22 07:23:05.184589-04	2021-03-22 07:23:05.184589-04		t
redswan796	$2b$12$j7b1ParatfAj34BfHeWuKOvQkDYIQ54KY5XdJm63NNPcU5CFffXPi	Oscar	Barbier	oscar.barbier@example.com	8868878888					f	2021-03-22 07:23:05.191767-04	2021-03-22 07:23:05.191767-04		t
purplerabbit786	$2b$12$osrP03kOhSGua8ZmeghuOOCLwaBwGM79tpBWzFR/vAgHLml7jLQvW	Alvarino	Lopes	alvarino.lopes@example.com	8868878888					f	2021-03-22 07:23:05.202124-04	2021-03-22 07:23:05.202124-04		t
lazyrabbit359	$2b$12$Y8Nbg3bb1vaEhQmJai/nq.M25DYn5JWUev.NoIKZGuNbMXctbgjYe	Amber	Caldwell	amber.caldwell@example.com	8868878888					f	2021-03-22 07:23:05.207714-04	2021-03-22 07:23:05.207714-04		t
reddog725	$2b$12$6EFbz42e3N2YZ1WnF4JodeowcP/GhPsnQj.iEhgaYKvDcjcQqMItW	Onur	Karaböcek	onur.karabocek@example.com	8868878888					f	2021-03-22 07:23:05.217796-04	2021-03-22 07:23:05.217796-04		t
tinylion731	$2b$12$iCZJc51IDs7pUYb7Z5jZmeWYvez0udbKvyyzVr7BCgSnBY4aW7vL2	Larry	Gilbert	larry.gilbert@example.com	8868878888					f	2021-03-22 07:23:05.224817-04	2021-03-22 07:23:05.224817-04		t
smallkoala113	$2b$12$yPae.SwvcM67iZeOWrEnBOYzpTk5mcX./gyFk5sHKgKVu0O2I3jha	Aubree	Ramos	aubree.ramos@example.com	8868878888					f	2021-03-22 07:23:05.235426-04	2021-03-22 07:23:05.235426-04		t
ticklishmeercat738	$2b$12$eUcYrovMnt8J3yxUEwO9AeL/MJPz7Z5Cy3CCGWPasZWZnFuF3tjt6	Arttu	Tuomi	arttu.tuomi@example.com	8868878888					f	2021-03-22 07:23:05.242278-04	2021-03-22 07:23:05.242278-04		t
crazyzebra393	$2b$12$aSL2Oih0JFuxU9eJw2lrneIeP50GpRohOdgSbRMtj6A1A2Awa7oJm	Ayşe	Hakyemez	ayse.hakyemez@example.com	8868878888					f	2021-03-22 07:23:05.253892-04	2021-03-22 07:23:05.253892-04		t
happyduck654	$2b$12$kF9SJ.jIAmSGi36pCEprx.AaFh4vW.575WlgsDR0CWxBvI/RldppG	Kenneth	Price	kenneth.price@example.com	8868878888					f	2021-03-22 07:23:05.258806-04	2021-03-22 07:23:05.258806-04		t
greenbutterfly908	$2b$12$SU7LSMDfYKjH36HHmcLEpeWgV0w7eLNqogRVSGJDxRuLQJcZFYcoa	Same	Thompson	same.thompson@example.com	8868878888					f	2021-03-22 07:23:05.268506-04	2021-03-22 07:23:05.268506-04		t
crazyelephant470	$2b$12$i7CX2Bb1KDmxWttF3nb0d.qTryTZbgH8/7ISVFdciK1ck7Y66h5U2	Cassandra	Sæterbø	cassandra.saeterbo@example.com	8868878888					t	2021-03-22 07:23:15.861369-04	2021-03-22 07:23:15.861369-04		t
silverwolf580	$2b$12$4mJLzzd4aWMbQklrSnUURegooISCIUMoee0Rpu12BW2pHTTptUMPy	Madison	Mitchell	madison.mitchell@example.com	8868878888					t	2021-03-22 07:23:15.86532-04	2021-03-22 07:23:15.86532-04		t
blackfrog937	$2b$12$p3Ek64IcIXh6cIhNJAv6k.aTNgnUgiPZm1RJfR/OXvTaIARnK39PG	Mandy	Olson	mandy.olson@example.com	8868878888					t	2021-03-22 07:23:15.873462-04	2021-03-22 07:23:15.873462-04		t
lazylion973	$2b$12$2zy/nxRfEgejvJSUFffoVu94I.srmsKRg9ZghRO.IxoTCPuJaoLs6	Tim	Laurent	tim.laurent@example.com	8868878888					t	2021-03-22 07:23:15.882551-04	2021-03-22 07:23:15.882551-04		t
bluebutterfly264	$2b$12$4HmrFk3fF/dPgI9hl2zrbucEM2rcGNiRrwx7a5DtHoFiGdeagxTfi	Iiris	Hokkanen	iiris.hokkanen@example.com	8868878888					t	2021-03-22 07:23:15.886289-04	2021-03-22 07:23:15.886289-04		t
bigmouse962	$2b$12$5qnWUbnP44C7K4WlO74krO7ee3SDqGBaxWxRcvcfT0CmdlGPKajx6	Beatriz	Velasco	beatriz.velasco@example.com	8868878888					t	2021-03-22 07:23:15.891644-04	2021-03-22 07:23:15.891644-04		t
organicfish120	$2b$12$L4FYWkX5ux8.g15Zk7JtGuzXjqWczKeTUM2BR0ZGPmV1YpRn/u/Rq	John	Brown	john.brown@example.com	8868878888					t	2021-03-22 07:23:15.899706-04	2021-03-22 07:23:15.899706-04		t
bigrabbit114	$2b$12$CAZkYN0KqM/nBdfGryiXG.apGAwxe3sa8dkXpbEwlGq/lJgLenj3C	Aksel	Nybakken	aksel.nybakken@example.com	8868878888					t	2021-03-22 07:23:15.904769-04	2021-03-22 07:23:15.904769-04		t
sadlion440	$2b$12$DB3mm8wwO8VS1nSY.pm31uVcXbyp/GR6aZRaLxtI8wSUKpfOtf1ei	Nicoline	Larsen	nicoline.larsen@example.com	8868878888					t	2021-03-22 07:23:15.909708-04	2021-03-22 07:23:15.909708-04		t
lazypeacock493	$2b$12$vWw7K/jxbJrojF0fuznR8eE9xevaZToZV4pRJts1O.osWbu69TG0K	Vanesa	Romero	vanesa.romero@example.com	8868878888					t	2021-03-22 07:23:15.916552-04	2021-03-22 07:23:15.916552-04		t
bigcat818	$2b$12$aIKxWJRl4o0lpxa7fVneGO76537gjDXCw8LT9WnDL5CrN7jFHe/Ni	Mio	Gaustad	mio.gaustad@example.com	8868878888					t	2021-03-22 07:23:15.922547-04	2021-03-22 07:23:15.922547-04		t
silverduck953	$2b$12$8XfZHVhXGTEdi8XEspOSt.qarMJZuE9WVtwAqQs/Uh0m5j0HdL/VS	Patricia	Warren	patricia.warren@example.com	8868878888					t	2021-03-22 07:23:15.933146-04	2021-03-22 07:23:15.933146-04		t
whitekoala828	$2b$12$qXZDQTFtj5ex11U/OTLPP.ex7qvCWqmcrEby4zSuza2mT1DVYfpdi	Toledo	Farias	toledo.farias@example.com	8868878888					t	2021-03-22 07:23:15.938821-04	2021-03-22 07:23:15.938821-04		t
whiteduck570	$2b$12$bNfhSP4P5Cc6W.F6IfApJuMEV0HSCrurgGjZvFn/kGpOvYIg9RT/u	Hans-Günther	Otte	hans-gunther.otte@example.com	8868878888					t	2021-03-22 07:23:15.943979-04	2021-03-22 07:23:15.943979-04		t
yellowostrich706	$2b$12$.opHQ871ju.nU2Bfb3UV4OU5iz7lftQDAcbO.kuhMc7mJVhi34/6S	Elif	Ilıcalı	elif.ilicali@example.com	8868878888					t	2021-03-22 07:23:15.950824-04	2021-03-22 07:23:15.950824-04		t
crazylion587	$2b$12$F73nGAJ2qWk8cpoEbnH6nupvAISEeA4ubUDSwmHSH/JRMljIdnGuW	Castelino	Pires	castelino.pires@example.com	8868878888					t	2021-03-22 07:23:15.956756-04	2021-03-22 07:23:15.956756-04		t
purplebird449	$2b$12$.6TdYFEErAeo6vbp5s2EUuYdeN2HyyFt7oxyugL3kTdl.vGY1m3hm	Pinja	Perala	pinja.perala@example.com	8868878888					t	2021-03-22 07:23:15.966712-04	2021-03-22 07:23:15.966712-04		t
heavypanda785	$2b$12$adyL07PzdQgUpu8uYDweQ.Q9XXqN.Crvw2lbdueCiLWlpprUNtYl2	Josh	West	josh.west@example.com	8868878888					t	2021-03-22 07:23:15.972728-04	2021-03-22 07:23:15.972728-04		t
browngorilla178	$2b$12$oA3WMkS6bRkiaBLx0GuaIutqUB1GMSo6lcMMxoBrc8yHuuxzbPLES	غزل	گلشن	gzl.glshn@example.com	8868878888					t	2021-03-22 07:23:15.977101-04	2021-03-22 07:23:15.977101-04		t
goldenbutterfly683	$2b$12$jD.sWZDmeA1bAtRaJYxr5Oz5nE8SNY8B7.B0g1LHSlIQhRdyWemEi	Eugenia	Molina	eugenia.molina@example.com	8868878888					t	2021-03-22 07:23:15.984193-04	2021-03-22 07:23:15.984193-04		t
bigpanda663	$2b$12$RPrMQZbmUYev67msRrkZVeN7xJ0Vm/xabIjWsYmZymOO/59dg90xy	Nicolas	Herrero	nicolas.herrero@example.com	8868878888					t	2021-03-22 07:23:15.990124-04	2021-03-22 07:23:15.990124-04		t
organicbird867	$2b$12$bHH5wmCmIsMgaa8E2HGG7eGrPaIoTxlcW/vx9wO6gk9HEaqSS9FNG	Maddison	Nelson	maddison.nelson@example.com	8868878888					t	2021-03-22 07:23:16.000078-04	2021-03-22 07:23:16.000078-04		t
blackelephant183	$2b$12$ssMPczq.VRxy.oBtQvpOG./QxhJvWfFyDm8BV/vqgGNrs.cJhbnGi	Annelie	Pieper	annelie.pieper@example.com	8868878888					t	2021-03-22 07:23:16.005604-04	2021-03-22 07:23:16.005604-04		t
bluedog478	$2b$12$AThZaaEqVH01A/tE.r2m0ebIa5fV6rVkloJxf/RjB2kVpxUQcOSBS	Coşkun	Koyuncu	coskun.koyuncu@example.com	8868878888					t	2021-03-22 07:23:16.017704-04	2021-03-22 07:23:16.017704-04		t
tinypanda585	$2b$12$MdsfennsG4fmbB4eAECfru/hFOuhBK7ZAOAM2kjqqgxtQmPBrhAXy	Milan	Van Gorkom	milan.vangorkom@example.com	8868878888					t	2021-03-22 07:23:16.023788-04	2021-03-22 07:23:16.023788-04		t
heavyladybug748	$2b$12$wp9uMUdiKcrEWwTvKniHhu/k.m33fRdqBEaxh6gQApH5PvG0U2f6C	Susann	Rutz	susann.rutz@example.com	8868878888					t	2021-03-22 07:23:16.033457-04	2021-03-22 07:23:16.033457-04		t
greenlion478	$2b$12$dL0wkhqV5Yaj7RPtlRp7X.I8BxFRAoAX6on7h5v0vsJjJt33dhZmC	Indie	White	indie.white@example.com	8868878888					t	2021-03-22 07:23:16.038651-04	2021-03-22 07:23:16.038651-04		t
blackgorilla620	$2b$12$VK8wdOx0SDB48Va6qgycAubGY.R2HK/KRlO/pMyL3UABg89MZi/Ay	Darren	Bishop	darren.bishop@example.com	8868878888					t	2021-03-22 07:23:16.043186-04	2021-03-22 07:23:16.043186-04		t
smallkoala709	$2b$12$9.zYrES.sWx4G9NIO32Ep.2HEcpx8FZHBiTRyiLq4a7JPjIphVM8a	Felicia	Bailey	felicia.bailey@example.com	8868878888					t	2021-03-22 07:23:16.051026-04	2021-03-22 07:23:16.051026-04		t
goldenladybug179	$2b$12$us.HAXBv0gfCss7FhMQ1GOK7NjxmNfol4UjJt/36J8KjX5btFqDJ6	Isabel	Gimenez	isabel.gimenez@example.com	8868878888					t	2021-03-22 07:23:16.056488-04	2021-03-22 07:23:16.056488-04		t
\.


--
-- Name: appointments_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sunbaowu
--

SELECT pg_catalog.setval('public.appointments_id_seq', 1, true);


--
-- Name: categories_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sunbaowu
--

SELECT pg_catalog.setval('public.categories_id_seq', 7, true);


--
-- Name: services_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sunbaowu
--

SELECT pg_catalog.setval('public.services_id_seq', 50, true);


--
-- Name: admins admins_pkey; Type: CONSTRAINT; Schema: public; Owner: sunbaowu
--

ALTER TABLE ONLY public.admins
    ADD CONSTRAINT admins_pkey PRIMARY KEY (username);


--
-- Name: appointments appointments_pkey; Type: CONSTRAINT; Schema: public; Owner: sunbaowu
--

ALTER TABLE ONLY public.appointments
    ADD CONSTRAINT appointments_pkey PRIMARY KEY (id);


--
-- Name: categories categories_pkey; Type: CONSTRAINT; Schema: public; Owner: sunbaowu
--

ALTER TABLE ONLY public.categories
    ADD CONSTRAINT categories_pkey PRIMARY KEY (id);


--
-- Name: categories_services categories_services_pkey; Type: CONSTRAINT; Schema: public; Owner: sunbaowu
--

ALTER TABLE ONLY public.categories_services
    ADD CONSTRAINT categories_services_pkey PRIMARY KEY (category_id, service_id);


--
-- Name: schedules schedules_pkey; Type: CONSTRAINT; Schema: public; Owner: sunbaowu
--

ALTER TABLE ONLY public.schedules
    ADD CONSTRAINT schedules_pkey PRIMARY KEY (username, date_exp);


--
-- Name: services services_pkey; Type: CONSTRAINT; Schema: public; Owner: sunbaowu
--

ALTER TABLE ONLY public.services
    ADD CONSTRAINT services_pkey PRIMARY KEY (id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: sunbaowu
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (username);


--
-- Name: appointments appointments_customer_username_fkey; Type: FK CONSTRAINT; Schema: public; Owner: sunbaowu
--

ALTER TABLE ONLY public.appointments
    ADD CONSTRAINT appointments_customer_username_fkey FOREIGN KEY (customer_username) REFERENCES public.users(username) ON DELETE CASCADE;


--
-- Name: appointments appointments_provider_username_fkey; Type: FK CONSTRAINT; Schema: public; Owner: sunbaowu
--

ALTER TABLE ONLY public.appointments
    ADD CONSTRAINT appointments_provider_username_fkey FOREIGN KEY (provider_username) REFERENCES public.users(username) ON DELETE CASCADE;


--
-- Name: appointments appointments_service_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: sunbaowu
--

ALTER TABLE ONLY public.appointments
    ADD CONSTRAINT appointments_service_id_fkey FOREIGN KEY (service_id) REFERENCES public.services(id) ON DELETE CASCADE;


--
-- Name: categories_services categories_services_category_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: sunbaowu
--

ALTER TABLE ONLY public.categories_services
    ADD CONSTRAINT categories_services_category_id_fkey FOREIGN KEY (category_id) REFERENCES public.categories(id) ON DELETE CASCADE;


--
-- Name: categories_services categories_services_service_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: sunbaowu
--

ALTER TABLE ONLY public.categories_services
    ADD CONSTRAINT categories_services_service_id_fkey FOREIGN KEY (service_id) REFERENCES public.services(id) ON DELETE CASCADE;


--
-- Name: schedules schedules_username_fkey; Type: FK CONSTRAINT; Schema: public; Owner: sunbaowu
--

ALTER TABLE ONLY public.schedules
    ADD CONSTRAINT schedules_username_fkey FOREIGN KEY (username) REFERENCES public.users(username) ON DELETE CASCADE;


--
-- Name: services services_username_fkey; Type: FK CONSTRAINT; Schema: public; Owner: sunbaowu
--

ALTER TABLE ONLY public.services
    ADD CONSTRAINT services_username_fkey FOREIGN KEY (username) REFERENCES public.users(username) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

