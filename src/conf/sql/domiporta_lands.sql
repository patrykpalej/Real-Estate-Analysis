CREATE TABLE public.domiporta_lands
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
    land_area smallint,
    driveway text,
    media text,
    PRIMARY KEY (number_id)
);
