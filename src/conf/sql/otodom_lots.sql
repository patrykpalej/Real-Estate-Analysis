CREATE TABLE public.otodom_lots
(
    number_id integer NOT NULL,
    short_id character varying(8) NOT NULL,
    long_id text NOT NULL,
    url text NOT NULL,
    title text NOT NULL,
    price integer NOT NULL,
    advertiser_type text,
    advert_type text,
    utc_created_at timestamp without time zone,
    utc_scraped_at timestamp without time zone,
    description text,
    city text,
    subregion text,
    province text,
    location text,
    latitude real,
    longitude real,
    lot_area smallint,
    lot_features text,
    vicinity text,
    PRIMARY KEY (number_id)
);
