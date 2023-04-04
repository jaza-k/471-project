
user_table = """CREATE TABLE IF NOT EXISTS _user (
    email VARCHAR(128),
    first_name VARCHAR(64),
    last_name VARCHAR(64),
    _address VARCHAR(128), 
    _city_name VARCHAR(128),
    _number_of_active_searches INT,
    PRIMARY KEY (email), 
    CONSTRAINT fk_city_name 
        FOREIGN KEY (_city_name) 
            REFERENCES city (_name) ON DELETE CASCADE
);"""


user_search_table = """
CREATE TABLE IF NOT EXISTS user_search 
(
    _sid VARCHAR(64) NOT NULL,
    _start_date timestamp(0) with time zone NOT NULL,
    _active BOOLEAN NOT NULL, 
    _email VARCHAR(100) NOT NULL, 
    origin_city VARCHAR(128) NOT NULL,
    PRIMARY KEY (_sid),
    CONSTRAINT fk_email 
        FOREIGN KEY (_email) 
            REFERENCES _user (email) ON DELETE CASCADE,
    CONSTRAINT fk_origin_city 
        FOREIGN KEY (origin_city) 
            REFERENCES city (_name) ON DELETE CASCADE
); """

scraped_ads_table = """
CREATE TABLE IF NOT EXISTS scraped_ads 
(
    _ad_id VARCHAR(64) NOT NULL, -- sha256 digest
    _ad_url VARCHAR(256) NOT NULL,
    _city VARCHAR (128) NOT NULL, 
    _date_added timestamp(0) NOT NULL,
    PRIMARY KEY (_ad_id),
    CONSTRAINT fk_city 
        FOREIGN KEY (_city)
            REFERENCES city (_name) ON DELETE CASCADE
);
"""


history_table = """
CREATE TABLE IF NOT EXISTS history
(
    _user_search_id VARCHAR(64) NOT NULL, 
    _deactivation_date timestamp(0) NOT NULL,
    CONSTRAINT fk_user_search_id 
        FOREIGN KEY (_user_search_id) 
            REFERENCES user_search (_sid) ON DELETE CASCADE
);
"""

matches_with_table = """CREATE TABLE IF NOT EXISTS matches_with
(
    _search_id VARCHAR(64) NOT NULL, 
    _matched_ad_id VARCHAR(64) NOT NULL, 
    CONSTRAINT fk_seach_id 
        FOREIGN KEY (_search_id) 
            REFERENCES user_search (_sid) ON DELETE CASCADE, 
    CONSTRAINT fk_matched_ad_id 
        FOREIGN KEY (_matched_ad_id) 
            REFERENCES scraped_ads (_ad_id) ON DELETE CASCADE
);
"""

ad_from_table = """
CREATE TABLE IF NOT EXISTS ad_from
(
    _from_ad_id VARCHAR(64) NOT NULL, 
    _origin_city VARCHAR(128) NOT NULL, 
    CONSTRAINT fk_from_ad_id 
        FOREIGN KEY (_from_ad_id) 
            REFERENCES scraped_ads (_ad_id) ON DELETE CASCADE,
    CONSTRAINT fk_origin_city 
        FOREIGN KEY (_origin_city) 
            REFERENCES city (_name) ON DELETE CASCADE
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
    __uuid VARCHAR(64) NOT NULL,        -- will be a sha256 digest 
    _search_type VARCHAR (32) NOT NULL, -- Bicycle / Motorcycle / Vehicle
    _make VARCHAR (256), 
    _model VARCHAR (256),
    _year INT, 
    _colour VARCHAR (32),
    _body_type VARCHAR (64), 

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
            REFERENCES country (_name) ON DELETE CASCADE, 
    CONSTRAINT fk_city_name 
        FOREIGN KEY (_city_name) 
            REFERENCES city (_name) ON DELETE CASCADE
);"""

scraped_references_table = """
CREATE TABLE IF NOT EXISTS scraped_references 
(
    _ad_id_origin VARCHAR(64) NOT NULL, 
    _ad_uuid VARCHAR(64) NOT NULL, 
    CONSTRAINT fk_ad_id_origin 
        FOREIGN KEY (_ad_id_origin) 
            REFERENCES scraped_ads (_ad_id) ON DELETE CASCADE, 
    CONSTRAINT fk_ad_uuid 
        FOREIGN KEY (_ad_uuid) 
            REFERENCES search_type (__uuid) ON DELETE CASCADE
); """

scraped_from = """
CREATE TABLE IF NOT EXISTS scraped_from 
(
    _ad_id_from VARCHAR(64) NOT NULL, 
    _marketplace_url VARCHAR (256), 
    CONSTRAINT fk_ad_id_from
        FOREIGN KEY (_ad_id_from) 
            REFERENCES scraped_ads (_ad_id) ON DELETE CASCADE, 
    CONSTRAINT fk_marketplace_url 
        FOREIGN KEY (_marketplace_url) 
            REFERENCES marketplace (_url) ON DELETE CASCADE
);
"""

user_references_table = """
CREATE TABLE IF NOT EXISTS user_references 
(
    _search_uuid VARCHAR(64) NOT NULL, 
    _user_search_id VARCHAR(64) NOT NULL, 
    CONSTRAINT fk_search_uuid 
        FOREIGN KEY (_search_uuid) 
            REFERENCES search_type (__uuid) ON DELETE CASCADE,
    CONSTRAINT fk_user_search_id 
        FOREIGN KEY (_user_search_id) 
            REFERENCES user_search (_sid) ON DELETE CASCADE
); """

available_in = """CREATE TABLE IF NOT EXISTS available_In
(
    _marketplace_url VARCHAR(256) NOT NULL, 
    _country VARCHAR(64) NOT NULL, 
    CONSTRAINT fk_marketplace_url
        FOREIGN KEY (_marketplace_url) 
            REFERENCES marketplace (_url) ON DELETE CASCADE, 
    CONSTRAINT fk_country
        FOREIGN KEY (_country) 
            REFERENCES country (_name) ON DELETE CASCADE
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
