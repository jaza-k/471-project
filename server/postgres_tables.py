
user_table = """CREATE TABLE IF NOT EXISTS _user (
    email VARCHAR(100),
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    _address VARCHAR(75), 
    _city_name VARCHAR(128),
    PRIMARY KEY (email), 
    CONSTRAINT fk_city_name 
        FOREIGN KEY (_city_name) 
            REFERENCES city (_name) 
);"""


user_search_table = """
CREATE TABLE IF NOT EXISTS user_search 
(
    _sid SERIAL,
    _start_date timestamp(0) with time zone NOT NULL,
    _active BOOLEAN NOT NULL, 
    _email VARCHAR(100) NOT NULL, 
    origin_city VARCHAR(128) NOT NULL,
    PRIMARY KEY (_sid),
    CONSTRAINT fk_email 
        FOREIGN KEY (_email) 
            REFERENCES _user (email),
    CONSTRAINT fk_origin_city 
        FOREIGN KEY (origin_city) 
            REFERENCES city (_name) 
); """

scraped_ads_table = """
CREATE TABLE IF NOT EXISTS scraped_ads 
(
    _ad_id SERIAL,
    _date_posted timestamp(0) NOT NULL,
    PRIMARY KEY (_ad_id)
);
"""


history_table = """
CREATE TABLE IF NOT EXISTS history
(
    _user_search_id SERIAL NOT NULL, 
    _deactivation_date timestamp(0) NOT NULL,
    CONSTRAINT fk_user_search_id 
        FOREIGN KEY (_user_search_id) 
            REFERENCES user_search (_sid)
);
"""

matches_with_table = """CREATE TABLE IF NOT EXISTS matches_with
(
    _search_id SERIAL NOT NULL, 
    _matched_ad_id SERIAL NOT NULL, 
    CONSTRAINT fk_seach_id 
        FOREIGN KEY (_search_id) 
            REFERENCES user_search (_sid), 
    CONSTRAINT fk_matched_ad_id 
        FOREIGN KEY (_matched_ad_id) 
            REFERENCES scraped_ads (_ad_id) 
);
"""

ad_from_table = """
CREATE TABLE IF NOT EXISTS ad_from
(
    _from_ad_id SERIAL NOT NULL, 
    _origin_city VARCHAR(128) NOT NULL, 
    CONSTRAINT fk_from_ad_id 
        FOREIGN KEY (_from_ad_id) 
            REFERENCES scraped_ads (_ad_id),
    CONSTRAINT fk_origin_city 
        FOREIGN KEY (_origin_city) 
            REFERENCES city (_name)
);"""

city_table = """CREATE TABLE IF NOT EXISTS city 
(
    _name VARCHAR(128) NOT NULL,
    PRIMARY KEY(_name)
);"""

country_table = """CREATE TABLE IF NOT EXISTS country
(
    _name VARCHAR(64) NOT NULL,
    PRIMARY KEY(_name)
);"""

search_type_table = """CREATE TABLE IF NOT EXISTS search_type
(
    __uuid uuid DEFAULT uuid_generate_v4() NOT NULL, 
    _search_type VARCHAR (32) NOT NULL, -- Bicycle / Motorcycle / Vehicle
    _make VARCHAR (256), 
    _model VARCHAR (256),
    _year INT, 
    _colour VARCHAR (32),
    _type VARCHAR (64), 

    PRIMARY KEY (__uuid)
);"""

marketplace_table = """CREATE TABLE IF NOT EXISTS marketplace
(
    _url VARCHAR (256) NOT NULL, 
    _name VARCHAR (128) NOT NULL, 
    PRIMARY KEY (_url) 
);"""

is_in_table = """CREATE TABLE IF NOT EXISTS is_in
(
    _country VARCHAR(64) NOT NULL, 
    _city_name VARCHAR(128) NOT NULL, 
    CONSTRAINT fk_county 
        FOREIGN KEY (_country) 
            REFERENCES country (_name), 
    CONSTRAINT fk_city_name 
        FOREIGN KEY (_city_name) 
            REFERENCES city (_name)
);"""

scraped_references_table = """
CREATE TABLE IF NOT EXISTS scraped_references 
(
    _ad_id_origin SERIAL NOT NULL, 
    _ad_uuid uuid NOT NULL, 
    CONSTRAINT fk_ad_id_origin 
        FOREIGN KEY (_ad_id_origin) 
            REFERENCES scraped_ads (_ad_id), 
    CONSTRAINT fk_ad_uuid 
        FOREIGN KEY (_ad_uuid) 
            REFERENCES search_type (__uuid)
); """

scraped_from = """
CREATE TABLE IF NOT EXISTS scraped_from 
(
    _ad_id_from SERIAL NOT NULL, 
    _marketplace_url VARCHAR (256), 
    CONSTRAINT fk_ad_id_from
        FOREIGN KEY (_ad_id_from) 
            REFERENCES scraped_ads (_ad_id), 
    CONSTRAINT fk_marketplace_url 
        FOREIGN KEY (_marketplace_url) 
            REFERENCES marketplace (_url)
);
"""

user_references_table = """
CREATE TABLE IF NOT EXISTS user_references 
(
    _search_uuid uuid NOT NULL, 
    _user_search_id SERIAL NOT NULL, 
    CONSTRAINT fk_search_uuid 
        FOREIGN KEY (_search_uuid) 
            REFERENCES search_type (__uuid),
    CONSTRAINT fk_user_search_id 
        FOREIGN KEY (_user_search_id) 
            REFERENCES user_search (_sid) 
); """

available_in = """CREATE TABLE IF NOT EXISTS available_In
(
    _marketplace_url VARCHAR(256) NOT NULL, 
    _country VARCHAR(64) NOT NULL, 
    CONSTRAINT fk_marketplace_url
        FOREIGN KEY (_marketplace_url) 
            REFERENCES marketplace (_url), 
    CONSTRAINT fk_country
        FOREIGN KEY (_country) 
            REFERENCES country (_name) 
);
"""

TABLE_NAMES = [
    "country",
    "city",
    "_user",
    "user_search",
    "scraped_ads",
    "history",
    "matches_with",
    "ad_from",
    "search_type",
    "marketplace",
    "is_in",
    "scraped_references",
    "scraped_from",
    "user_references",
    "available_in"
]

TABLES_CREATE_QUERIES = [
    country_table,
    city_table,
    user_table, 
    user_search_table, 
    scraped_ads_table, 
    history_table, 
    matches_with_table, 
    ad_from_table,
    search_type_table,
    marketplace_table,
    is_in_table,
    scraped_references_table,
    scraped_from,
    user_references_table,
    available_in
    ]
