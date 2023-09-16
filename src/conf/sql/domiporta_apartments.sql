CREATE TABLE public.domiporta_apartments
(
    number_id text NOT NULL,
    url text NOT NULL,
    title text NOT NULL,
    price integer NOT NULL,
    utc_scraped_at timestamp without time zone,
    description text,
    city text,
    province text,
    latitude real,
    longitude real,
    area numeric,
    build_year smallint,
    n_rooms smallint,
    PRIMARY KEY (number_id)
);
