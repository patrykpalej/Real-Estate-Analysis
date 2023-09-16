CREATE TABLE public.domiporta_houses
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
    lot_area smallint,
    driveway text,
    media text,
    area numeric,
    build_year smallint,
    n_rooms smallint,
    building_type text,

    PRIMARY KEY (number_id)
);
