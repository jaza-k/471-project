# import dsn 
import psycopg2 
import re 
from hashlib import sha256
from datetime import datetime

"""
Instead of using Postgres' SERIAL and UUID, create a unique identifier by 
concatenating relevant information togather and creating a sha256 digest

this should create unique identifier that does not produce collisions 
with high probability (attempts until collision being 2^128)

for creating the uuid for user_search : 
    uuid_user = sha256 ( email || search_number || time_of_search ) 
    
for creating the uuid for scraped ads : 
    uuid_ad = sha256 ( ad_id || ad_url ) 
    
parameters to be concatenated are passed as a list of strings 

for creating the uuid for search types: 

    if search type is a active user search: 
        
        uuid = sha256 ( uuid_user || all_attributes )
    
    else if the search type is a scraped ad

        uuid = sha256 ( uuid_ad || all_attributes )

these are then uniform uuids that can be used for the search_type tables uuid atetribute 

"""
def create_uuid(params)->str:
    _msg = ""
    
    for p in  params:
        _msg += str(p)      # incase not everything is a string when passed in 
    
    _msg_bytes = bytes(_msg, "UTF-8")
    h = sha256(_msg_bytes).hexdigest()
    
    return h 

# https://stackoverflow.com/questions/1323364/in-python-how-to-check-if-a-string-only-contains-certain-characters

def check_field(attr:str):
    okay_chars = re.compile('^[0-9a-zA-Z@. ]').search            # create a function from the pattern 
    return bool(okay_chars(attr)) 


def check_country_city_exists(curs, _country:str, _city:str):
    
    # make lowercase so all is uniform in the tables 
    city = _city.lower()
    country = _country.lower()
    
    # check to see that country and city exists already 
    _q_check = f"SELECT COUNT(*) FROM is_in WHERE is_in._country = '{country}' AND is_in._city_name= '{city}';"
    curs.execute(_q_check)
    res = curs.fetchone()
    
    # res should be (1) so res[0] should just be one if 
    if res[0] != 1:
        country_check = f"SELECT COUNT(*) FROM country WHERE country._name = '{country}';"
        city_check = f"SELECT COUNT(*) FROM city WHERE city._name = '{city}';"
        
        curs.execute(city_check)
        res = curs.fetchone()
        if res[0] != 1:
            curs.execute("INSERT INTO city VALUES (%s)", (city,))
            
        curs.execute(country_check)
        res = curs.fetchone()
        if res[0] != 1:
            curs.execute("INSERT INTO country VALUES (%s)", (country,)) 
            
        
        curs.execute("INSERT INTO is_in VALUES (%s, %s)", (country, city))
        
    # else nothing needs to be done if they already exists 
    
def new_user_info(email, fname, lname, address, city, country, conn):
    
    # check types to make sure they are strings and stop injections 
    assert type(email) == str   and check_field(email),     "email is not valid"
    assert type(fname) == str   and check_field(fname),     "first name is not valid"
    assert type(lname) == str   and check_field(lname),     "last name is not valid"
    assert type(address) == str and check_field(address),   "address is not valid"
    assert type(city) == str    and check_field(city),      "city is not valid"
    assert type(country) == str and check_field(country),   "country is not valid"
    
    # get db conn objects 
    # conn = psycopg2.connect(dsn.DSN)
    curs = conn.cursor() 
    
    # check city and country already are in the db 
    check_country_city_exists(curs, country, city) 
    
    # insert new user into db 
    curs.execute("INSERT INTO _user VALUES (%s, %s, %s, %s, %s, %s)", 
                 (email, fname, lname, address, city, 0)
                )
    
    conn.commit()
    
    curs.close()
    # conn.close()
    
    # print("success")
    


# FOR LOGGING IN A USER 
def check_user_credentials(email, password, conn):
    curs = conn.cursor()

    # Replace 'password' with the appropriate column name in your '_user' table
    curs.execute("SELECT password FROM _user WHERE email = %s", (email,))
    result = curs.fetchone()

    if result:
        stored_password = result[0]
        # Compare the stored password with the provided password
        if stored_password == password:
            return True

    return False



def check_search_object(search_object:dict) -> bool:
    for (_, v) in search_object.items():
        
        if type(v) != str:      return False 
        if not check_field(v):  return False 
        
    return True 
    
    
def new_user_search(search_object:dict, email:str, origin_city:str, conn):
    assert check_search_object(search_object), "invalid inputs"
    
    # get db conn 
    # conn = psycopg2.connect(dsn.DSN) 
    curs = conn.cursor()
    
    # first update number of user searches and create entry in active searches table 
    usr_searches_q = f"SELECT u._number_of_active_searches FROM _user as u WHERE u.email='{email}';" 
    curs.execute(usr_searches_q)
    searches = curs.fetchone()
    if searches == None or len(searches) == 0:
        raise Exception("email does not exist in the DataBase")
    
    active_searches = searches[0]
    active_searches += 1
    
    current_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    # create uuid for the active user search 
    usr_search_uuid = create_uuid([email, active_searches, current_time])
    
    insert_usr_search = "INSERT INTO user_search VALUES (%s, %s, %s, %s, %s, %s)"
    insert_usr_tuple = (usr_search_uuid, current_time, True, email, origin_city, active_searches)
    
    curs.execute(insert_usr_search, insert_usr_tuple)
    
    curs.execute(f"UPDATE _user SET _number_of_active_searches = {active_searches} WHERE email = '{email}';")
    
    # for simplicity for now, assume we are only accepting vehicles and motorcycles right now 
    search_type_insert = "INSERT INTO search_type VALUES (%s, %s, %s, %s, %s, %s, %s)"
    search_type_uuid = create_uuid([usr_search_uuid] + list(search_object.values()))
    
    if search_object["search_type"] == "Vehicle":
        to_add = (
            search_type_uuid,
            search_object["search_type"],
            search_object["make"],
            search_object["model"],
            search_object["year"], 
            search_object["colour"],
            search_object["body_type"]
        )
        
    elif search_object["search_type"] == "Motorcycle":
        to_add = (
            search_type_uuid, 
            search_object["search_type"],
            search_object["make"],
            search_object["model"],
            search_object["year"], 
            search_object["colour"], 
            ""
        )
         
    elif search_object["search_type"] == "Bicycle":
        ...
    
    curs.execute(search_type_insert, to_add)
    
    # add entry to user_references table 
    user_references_q = "INSERT INTO user_references VALUES (%s, %s)"
    user_references_tuple = (search_type_uuid, usr_search_uuid)
    curs.execute(user_references_q, user_references_tuple) 
        
    
    conn.commit()
    curs.close()
    
    # conn.close()
    
def extract_marketplace_name(url:str):
    _match = re.search(r'www\.(\w+)\.', url)
    name = _match.group(1)
    return name 
        
def check_marketplace(curs, marketplace_url:str, _country:str):
    country = _country.lower()
    q_check = f"SELECT COUNT(*) FROM marketplace WHERE marketplace._url = '{marketplace_url}';"
    curs.execute(q_check)
    res = curs.fetchone()
    
    if res[0] != 1:
        marketplace_name = extract_marketplace_name(marketplace_url)
        insert_q = "INSERT INTO marketplace VALUES (%s, %s)"
        insert_tuple = (marketplace_url, marketplace_name)
        curs.execute(insert_q, insert_tuple)
        
    q_check_available_in = f"""
        SELECT 
            COUNT(*) 
        FROM 
            available_in AS ai
        WHERE 
            ai._marketplace_url = '{marketplace_url}' AND 
            ai._country = '{country}';
        """
    curs.execute(q_check_available_in)
    res = curs.fetchone()
    
    if res[0] != 1:
        insert_q = "INSERT INTO available_in VALUES (%s, %s)"
        insert_tuple = (marketplace_url, country)
        curs.execute(insert_q, insert_tuple)
    
        
def check_ad_already_exists(curs, uuid:str) -> bool:
    q = f"SELECT COUNT(*) FROM scraped_ads WHERE _ad_id = '{uuid}';"
    curs.execute(q)
    res = curs.fetchone()
    if res[0] == 1:
        return True 
    
    return False 


def new_scraped_ad(scrap_object:dict, ad_type:str, marketplace_url:str, conn):
    # conn = psycopg2.connect(dsn.DSN)
    curs = conn.cursor()
    
    ### first create the entry in the scraped ads table ### 
    
    # check that city country pair exists already in the db 
    _city = scrap_object["CITY"]
    _country = scrap_object["COUNTRY"]
    check_country_city_exists(curs, _country, _city)
    
    # check that the marketplace is already in the db 
    # along with available in for marketplace and country 
    check_marketplace(curs, marketplace_url, _country) 
    
    # create uuid 
    _ad_url = scrap_object["AD URL"]
    _ad_id = scrap_object["AD ID"]
    uuid_scraped_ad = create_uuid([_ad_id, _ad_url]) 
    
    # we don't need to do anything else if the id exists (assuming this is not a strong collision)
    if check_ad_already_exists(curs, uuid_scraped_ad):
        return None 
    
    time_stamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    insert_scraped = "INSERT INTO scraped_ads VALUES (%s, %s, %s, %s)"
    insert_scraped_tuple = (uuid_scraped_ad, _ad_url, _city, time_stamp) 
    curs.execute(insert_scraped, insert_scraped_tuple) 
    
    ### insert into search type the scraped ads' information ###
    
    search_type_insert = "INSERT INTO search_type VALUES (%s,%s,%s,%s,%s,%s,%s)"
    
    search_type_uuid = create_uuid([uuid_scraped_ad] + list(scrap_object.values()))
    
    # if there is no year then dedault to None 
    scrap_object["YEAR"] = None if scrap_object["YEAR"] == '' else scrap_object["YEAR"]
    
    if ad_type == "Vehicle":
        to_add = (
            search_type_uuid, 
            ad_type, 
            scrap_object["MAKE"], 
            scrap_object["MODEL"],
            scrap_object["YEAR"],
            scrap_object["COLOR"], 
            scrap_object["BODY TYPE"]
        )
        
    elif ad_type == "Motorcycle":
        to_add = (
            search_type_uuid, 
            ad_type, 
            scrap_object["MAKE"], 
            scrap_object["MODEL"],
            scrap_object["YEAR"],
            scrap_object["COLOR"],
            ""
        )
    elif ad_type == "Bicycle":
        ...
        
    curs.execute(search_type_insert, to_add)
    
    # add entry to scraped_references table 
    scraped_references_q = "INSERT INTO scraped_references VALUES (%s, %s)"
    scraped_references_tuple = (uuid_scraped_ad, search_type_uuid)
    curs.execute(scraped_references_q, scraped_references_tuple)
    
    # add entry to scraped_from table 
    scraped_from_q = "INSERT INTO scraped_from VALUES (%s, %s)"
    scraped_from_tuple = (uuid_scraped_ad, marketplace_url)
    curs.execute(scraped_from_q, scraped_from_tuple)
    
    # add entry to ad_from table 
    ad_from_q = "INSERT INTO ad_from VALUES (%s, %s)"
    ad_from_tuple = (uuid_scraped_ad, _city)
    curs.execute(ad_from_q, ad_from_tuple)
    
    conn.commit()
    curs.close()
    
    # conn.close()


if __name__ == "__main__":
    ...