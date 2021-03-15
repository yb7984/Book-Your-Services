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


ALTER TABLE public.schedules OWNER TO sunbaowu;

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
    email character varying(30) NOT NULL,
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



--
-- Name: appointments id; Type: DEFAULT; Schema: public; Owner: sunbaowu
--

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
admin	$2b$12$us8auv6mpCEn9jBY2uDRU.lTFH9qB0DSEnohoW8lvVAogzWeztGa.	admin	admin	bobowu@outlook.com	administrator	2021-03-15 09:08:23.536712-04		t
\.


--
-- Data for Name: appointments; Type: TABLE DATA; Schema: public; Owner: sunbaowu
--

COPY public.appointments (id, event_id, provider_username, customer_username, start, "end", service_id, note, updated, created, is_active) FROM stdin;
\.


--
-- Data for Name: categories; Type: TABLE DATA; Schema: public; Owner: sunbaowu
--

COPY public.categories (id, name, is_active) FROM stdin;
\.


--
-- Data for Name: categories_services; Type: TABLE DATA; Schema: public; Owner: sunbaowu
--

COPY public.categories_services (category_id, service_id) FROM stdin;
\.


--
-- Data for Name: schedules; Type: TABLE DATA; Schema: public; Owner: sunbaowu
--

COPY public.schedules (username, date_exp, schedules, is_active) FROM stdin;
\.


--
-- Data for Name: services; Type: TABLE DATA; Schema: public; Owner: sunbaowu
--

COPY public.services (id, username, name, description, image, updated, created, is_active) FROM stdin;
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: sunbaowu
--

COPY public.users (username, password, first_name, last_name, email, phone, description, image, calendar_id, calendar_email, is_provider, updated, created, pwd_token, is_active) FROM stdin;
\.


--
-- Name: appointments_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sunbaowu
--

SELECT pg_catalog.setval('public.appointments_id_seq', 1, false);


--
-- Name: categories_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sunbaowu
--

SELECT pg_catalog.setval('public.categories_id_seq', 1, false);


--
-- Name: services_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sunbaowu
--

SELECT pg_catalog.setval('public.services_id_seq', 1, false);


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

