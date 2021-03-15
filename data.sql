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
    email character varying(30) NOT NULL,
    "authorization" character varying(100) DEFAULT 'regular'::character varying NOT NULL,
    created timestamp with time zone DEFAULT now() NOT NULL,
    pwd_token text,
    is_active boolean DEFAULT true NOT NULL
);


ALTER TABLE public.admins OWNER TO sunbaowu;

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


ALTER TABLE public.appointments OWNER TO sunbaowu;

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


ALTER TABLE public.appointments_id_seq OWNER TO sunbaowu;

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


ALTER TABLE public.categories OWNER TO sunbaowu;

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


ALTER TABLE public.categories_id_seq OWNER TO sunbaowu;

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


ALTER TABLE public.categories_services OWNER TO sunbaowu;

--
-- Name: emails; Type: TABLE; Schema: public; Owner: sunbaowu
--

CREATE TABLE public.emails (
    id integer NOT NULL,
    appointment_id integer,
    sender_username character varying(20),
    receiver_username character varying(20),
    email character varying(30) NOT NULL,
    title character varying(100) NOT NULL,
    content text NOT NULL,
    is_sent boolean DEFAULT false NOT NULL,
    sent timestamp with time zone,
    created timestamp with time zone DEFAULT now() NOT NULL,
    is_active boolean DEFAULT true NOT NULL
);


ALTER TABLE public.emails OWNER TO sunbaowu;

--
-- Name: emails_id_seq; Type: SEQUENCE; Schema: public; Owner: sunbaowu
--

CREATE SEQUENCE public.emails_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.emails_id_seq OWNER TO sunbaowu;

--
-- Name: emails_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sunbaowu
--

ALTER SEQUENCE public.emails_id_seq OWNED BY public.emails.id;


--
-- Name: reviews; Type: TABLE; Schema: public; Owner: sunbaowu
--

CREATE TABLE public.reviews (
    id integer NOT NULL,
    appointment_id integer,
    from_username character varying(20),
    to_username character varying(20),
    rating integer NOT NULL,
    title character varying(100) NOT NULL,
    content text NOT NULL,
    is_visible boolean DEFAULT false NOT NULL,
    updated timestamp with time zone,
    created timestamp with time zone DEFAULT now() NOT NULL,
    is_active boolean DEFAULT true NOT NULL
);


ALTER TABLE public.reviews OWNER TO sunbaowu;

--
-- Name: reviews_id_seq; Type: SEQUENCE; Schema: public; Owner: sunbaowu
--

CREATE SEQUENCE public.reviews_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.reviews_id_seq OWNER TO sunbaowu;

--
-- Name: reviews_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sunbaowu
--

ALTER SEQUENCE public.reviews_id_seq OWNED BY public.reviews.id;


--
-- Name: schedules; Type: TABLE; Schema: public; Owner: sunbaowu
--

CREATE TABLE public.schedules (
    username character varying(20) NOT NULL,
    date_exp character varying(20) NOT NULL,
    schedules text DEFAULT ''::text NOT NULL,
    is_active boolean DEFAULT true NOT NULL
);


ALTER TABLE public.schedules OWNER TO sunbaowu;

--
-- Name: services; Type: TABLE; Schema: public; Owner: sunbaowu
--

CREATE TABLE public.services (
    id integer NOT NULL,
    username character varying(20),
    name character varying(100) NOT NULL,
    description text NOT NULL,
    image text,
    updated timestamp with time zone DEFAULT now() NOT NULL,
    created timestamp with time zone DEFAULT now() NOT NULL,
    is_active boolean DEFAULT true NOT NULL
);


ALTER TABLE public.services OWNER TO sunbaowu;

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


ALTER TABLE public.services_id_seq OWNER TO sunbaowu;

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
    email character varying(30) NOT NULL,
    phone character varying(20),
    description text,
    image text,
    calendar_id text,
    calendar_email character varying(50),
    reviews integer DEFAULT 0,
    rating double precision DEFAULT '0'::double precision,
    is_provider boolean DEFAULT false NOT NULL,
    updated timestamp with time zone DEFAULT now() NOT NULL,
    created timestamp with time zone DEFAULT now() NOT NULL,
    pwd_token text,
    is_active boolean DEFAULT true NOT NULL
);


ALTER TABLE public.users OWNER TO sunbaowu;

--
-- Name: appointments id; Type: DEFAULT; Schema: public; Owner: sunbaowu
--

ALTER TABLE ONLY public.appointments ALTER COLUMN id SET DEFAULT nextval('public.appointments_id_seq'::regclass);


--
-- Name: categories id; Type: DEFAULT; Schema: public; Owner: sunbaowu
--

ALTER TABLE ONLY public.categories ALTER COLUMN id SET DEFAULT nextval('public.categories_id_seq'::regclass);


--
-- Name: emails id; Type: DEFAULT; Schema: public; Owner: sunbaowu
--

ALTER TABLE ONLY public.emails ALTER COLUMN id SET DEFAULT nextval('public.emails_id_seq'::regclass);


--
-- Name: reviews id; Type: DEFAULT; Schema: public; Owner: sunbaowu
--

ALTER TABLE ONLY public.reviews ALTER COLUMN id SET DEFAULT nextval('public.reviews_id_seq'::regclass);


--
-- Name: services id; Type: DEFAULT; Schema: public; Owner: sunbaowu
--

ALTER TABLE ONLY public.services ALTER COLUMN id SET DEFAULT nextval('public.services_id_seq'::regclass);


--
-- Data for Name: admins; Type: TABLE DATA; Schema: public; Owner: sunbaowu
--

COPY public.admins (username, password, first_name, last_name, email, "authorization", created, pwd_token, is_active) FROM stdin;
admin	$2b$12$B2K1v9BgjYJUWrimaKB8OeC0abKYr.rKJSSuA9c4FWbEJ3WLuXoTq	admin	admin	bobowu@outlook.com	administrator	2021-03-02 15:02:29.606833-05	\N	t
\.


--
-- Data for Name: appointments; Type: TABLE DATA; Schema: public; Owner: sunbaowu
--

COPY public.appointments (id, event_id, provider_username, customer_username, start, "end", service_id, note, updated, created, is_active) FROM stdin;
1		test	test1	2021-03-07 19:30:00-05	2021-03-07 20:30:00-05	4	test teste	2021-03-07 06:39:20.389911-05	2021-03-07 06:39:20.389911-05	f
3	e8k8ma826cuajmno9s02amhubs	test	test1	2021-03-07 19:30:00-05	2021-03-07 20:30:00-05	4	tetwewrwe	2021-03-07 15:55:32.720241-05	2021-03-07 15:55:32.720241-05	t
4	gtb6tto8bpf4oa9ihejtu6c46o	test	test1	2021-03-08 21:30:00-05	2021-03-08 22:30:00-05	1	redrewterwrew	2021-03-07 15:56:14.228849-05	2021-03-07 15:56:14.228849-05	t
2		test	test1	2021-03-07 21:30:00-05	2021-03-07 22:30:00-05	4	test test22222	2021-03-07 15:55:01.863775-05	2021-03-07 15:55:01.863775-05	f
5	7p5qjsnajorkb3pu91n9f1rbrg	test	test1	2021-03-09 21:30:00-05	2021-03-09 22:30:00-05	4	test\r\ndfdfd	2021-03-08 22:46:28.407418-05	2021-03-08 22:46:28.407418-05	t
6		test	test1	2021-03-09 19:30:00-05	2021-03-09 20:30:00-05	4		2021-03-09 05:47:01.472552-05	2021-03-09 05:47:01.472552-05	t
7	1k583jmm1l3omd4bq7pf2mbm64	test	test1	2021-03-10 19:30:00-05	2021-03-10 20:30:00-05	4		2021-03-09 05:48:10.585918-05	2021-03-09 05:48:10.585918-05	t
8	bu6mn6i4g0i0v9ubhsgkvhchfs	test	test1	2021-03-10 21:30:00-05	2021-03-10 22:30:00-05	4		2021-03-09 05:52:15.462616-05	2021-03-09 05:52:15.462616-05	t
9	r0pnmkrg0oqajjus3tg3fqn50o	test2	test1	2021-03-10 09:40:00-05	2021-03-10 10:14:00-05	5	test note	2021-03-10 07:14:16.025688-05	2021-03-10 07:14:16.025688-05	t
10	dqd8k3l3lumagtdsf97mkrcj84	test	test2	2021-03-14 18:30:00-04	2021-03-14 19:30:00-04	4	test	2021-03-13 23:49:44.056301-05	2021-03-13 23:49:44.056301-05	t
\.


--
-- Data for Name: categories; Type: TABLE DATA; Schema: public; Owner: sunbaowu
--

COPY public.categories (id, name, is_active) FROM stdin;
3	Finance	t
1	Insurance	t
2	Tax	t
4	gggg333	t
\.


--
-- Data for Name: categories_services; Type: TABLE DATA; Schema: public; Owner: sunbaowu
--

COPY public.categories_services (category_id, service_id) FROM stdin;
3	1
1	1
1	4
2	4
3	4
3	5
1	5
1	6
2	6
\.


--
-- Data for Name: emails; Type: TABLE DATA; Schema: public; Owner: sunbaowu
--

COPY public.emails (id, appointment_id, sender_username, receiver_username, email, title, content, is_sent, sent, created, is_active) FROM stdin;
\.


--
-- Data for Name: reviews; Type: TABLE DATA; Schema: public; Owner: sunbaowu
--

COPY public.reviews (id, appointment_id, from_username, to_username, rating, title, content, is_visible, updated, created, is_active) FROM stdin;
\.


--
-- Data for Name: schedules; Type: TABLE DATA; Schema: public; Owner: sunbaowu
--

COPY public.schedules (username, date_exp, schedules, is_active) FROM stdin;
test	2021-03-19	[{"start": "09:21", "end": "10:21"}]	t
test	0	[{"start": "18:30", "end": "19:30"}, {"start": "19:30", "end": "20:30"}, {"start": "21:30", "end": "22:30"}]	t
test	3	[{"start": "18:30", "end": "19:30"}, {"start": "19:30", "end": "20:30"}, {"start": "21:30", "end": "22:30"}]	t
test	4	[{"start": "18:30", "end": "19:30"}, {"start": "19:30", "end": "20:30"}, {"start": "21:30", "end": "22:30"}]	t
test	5	[{"start": "18:30", "end": "19:30"}, {"start": "19:30", "end": "20:30"}, {"start": "21:30", "end": "22:30"}, {"start": "23:00", "end": "23:48"}]	t
test	2	[{"start": "19:30", "end": "20:30"}, {"start": "21:30", "end": "22:30"}]	t
test	2021-03-25	[{"start": "09:21", "end": "10:21"}]	t
test	1	[{"start": "19:30", "end": "20:30"}, {"start": "21:30", "end": "22:30"}]	t
test2	2	[{"start": "09:40", "end": "10:14"}, {"start": "11:12", "end": "12:12"}]	t
test2	3	[{"start": "09:40", "end": "10:14"}, {"start": "11:12", "end": "12:12"}]	t
test2	4	[{"start": "09:40", "end": "10:14"}, {"start": "11:12", "end": "12:12"}]	t
test2	6	[{"start": "09:40", "end": "10:14"}, {"start": "11:12", "end": "12:12"}]	t
test2	0	[{"start": "09:40", "end": "10:14"}, {"start": "11:12", "end": "12:12"}, {"start": "20:12", "end": "21:12"}]	t
test2	1	[{"start": "09:40", "end": "10:14"}, {"start": "11:12", "end": "12:12"}, {"start": "20:12", "end": "21:12"}]	t
test2	5	[{"start": "09:40", "end": "10:14"}, {"start": "11:12", "end": "12:12"}, {"start": "20:12", "end": "21:12"}]	t
\.


--
-- Data for Name: services; Type: TABLE DATA; Schema: public; Owner: sunbaowu
--

COPY public.services (id, username, name, description, image, updated, created, is_active) FROM stdin;
4	test	ggg	gg	\N	2021-03-06 17:13:29.766028-05	2021-03-06 06:52:19.148858-05	t
5	test2	testaaa	test	\N	2021-03-10 07:11:17.489916-05	2021-03-10 07:11:17.489923-05	t
6	test	test	aaaaa	\N	2021-03-13 23:46:34.338707-05	2021-03-13 23:35:11.167816-05	f
1	test	test	test	\N	2021-03-06 06:48:38.822104-05	2021-03-06 06:39:18.248382-05	f
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: sunbaowu
--

COPY public.users (username, password, first_name, last_name, email, phone, description, image, calendar_id, calendar_email, reviews, rating, is_provider, updated, created, pwd_token, is_active) FROM stdin;
test1	$2b$12$QkJIZE3uR64CvG1qppzjVOYQVz8aSsioegtUH8rMFWHpav0yUO3Tu			ybdevs.com@gmail.com			\N	\N	\N	0	0	f	2021-03-06 07:09:51.094312-05	2021-03-06 07:09:51.094312-05	\N	t
test3	$2b$12$1syGDVty12cui9YXEMSatuZOMCgySclOUj/KTMrFbn7RcUhwgWKq2			test@ybdevs.com			\N	\N	\N	0	0	f	2021-03-12 00:07:25.02474-05	2021-03-12 00:07:25.02474-05	\N	t
test	$2b$12$MD/bccRyL/571XaChjAbX.YPamicQLSrACnjpi6aUIEbPkrzXlWNW	Test	Test	bobowu@outlook.com	8603191969	Go gogogo	test.jpg	95s59t15qukqtd00777idts2b8@group.calendar.google.com	bobowu98@gmail.com	0	0	t	2021-03-08 23:12:20.969032-05	2021-03-02 15:05:49.054579-05	h1HltJ84q6muhDlKDnOsSOcyI4q_L2fHvF-2Dqxc1VU	t
test2	$2b$12$o/UdZEEhea94Qwi77fGkc.GmZCZixsW3mFXRrWzzGenh1qvO7.fMC	test		bobowu98@gmail.com			\N	fmj89k7132eu8qkf0091prp5b8@group.calendar.google.com	bobowu98@gmail.com	0	0	t	2021-03-12 15:02:31.215562-05	2021-03-10 07:07:02.876314-05	\N	t
\.


--
-- Name: appointments_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sunbaowu
--

SELECT pg_catalog.setval('public.appointments_id_seq', 10, true);


--
-- Name: categories_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sunbaowu
--

SELECT pg_catalog.setval('public.categories_id_seq', 4, true);


--
-- Name: emails_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sunbaowu
--

SELECT pg_catalog.setval('public.emails_id_seq', 1, false);


--
-- Name: reviews_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sunbaowu
--

SELECT pg_catalog.setval('public.reviews_id_seq', 1, false);


--
-- Name: services_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sunbaowu
--

SELECT pg_catalog.setval('public.services_id_seq', 6, true);


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
-- Name: emails emails_pkey; Type: CONSTRAINT; Schema: public; Owner: sunbaowu
--

ALTER TABLE ONLY public.emails
    ADD CONSTRAINT emails_pkey PRIMARY KEY (id);


--
-- Name: reviews reviews_pkey; Type: CONSTRAINT; Schema: public; Owner: sunbaowu
--

ALTER TABLE ONLY public.reviews
    ADD CONSTRAINT reviews_pkey PRIMARY KEY (id);


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
-- Name: emails emails_appointment_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: sunbaowu
--

ALTER TABLE ONLY public.emails
    ADD CONSTRAINT emails_appointment_id_fkey FOREIGN KEY (appointment_id) REFERENCES public.appointments(id) ON DELETE CASCADE;


--
-- Name: emails emails_receiver_username_fkey; Type: FK CONSTRAINT; Schema: public; Owner: sunbaowu
--

ALTER TABLE ONLY public.emails
    ADD CONSTRAINT emails_receiver_username_fkey FOREIGN KEY (receiver_username) REFERENCES public.users(username) ON DELETE CASCADE;


--
-- Name: emails emails_sender_username_fkey; Type: FK CONSTRAINT; Schema: public; Owner: sunbaowu
--

ALTER TABLE ONLY public.emails
    ADD CONSTRAINT emails_sender_username_fkey FOREIGN KEY (sender_username) REFERENCES public.users(username) ON DELETE CASCADE;


--
-- Name: reviews reviews_appointment_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: sunbaowu
--

ALTER TABLE ONLY public.reviews
    ADD CONSTRAINT reviews_appointment_id_fkey FOREIGN KEY (appointment_id) REFERENCES public.appointments(id) ON DELETE CASCADE;


--
-- Name: reviews reviews_from_username_fkey; Type: FK CONSTRAINT; Schema: public; Owner: sunbaowu
--

ALTER TABLE ONLY public.reviews
    ADD CONSTRAINT reviews_from_username_fkey FOREIGN KEY (from_username) REFERENCES public.users(username) ON DELETE CASCADE;


--
-- Name: reviews reviews_to_username_fkey; Type: FK CONSTRAINT; Schema: public; Owner: sunbaowu
--

ALTER TABLE ONLY public.reviews
    ADD CONSTRAINT reviews_to_username_fkey FOREIGN KEY (to_username) REFERENCES public.users(username) ON DELETE CASCADE;


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

