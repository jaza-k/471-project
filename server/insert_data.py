import dsn 
import psycopg2 
import re 


# https://stackoverflow.com/questions/1323364/in-python-how-to-check-if-a-string-only-contains-certain-characters

def check_field(attr:str):
    okay_chars = re.compile('^[0-9a-zA-Z@. ]').search            # create a function from the pattern 
    return bool(okay_chars(attr)) 


def check_country_city_exists(curs, country, city):
    # check to see that country and city exists already 
    _q_check = f"SELECT COUNT(*) FROM is_in WHERE is_in._country = '{country}' AND is_in._city_name= '{city}';"
    curs.execute(_q_check)
    res = curs.fetchone()
    
    # res should be (1) so res[0] should just be one if 
    if res[0] != 1:
        curs.execute("INSERT INTO city VALUES (%s)", (city,))
        curs.execute("INSERT INTO country VALUES (%s)", (country,)) 
        curs.execute("INSERT INTO is_in VALUES (%s, %s)", (country, city))
        
    # else nothing needs to be done if they already exists 
    
def new_user_info(email, fname, lname, address, city, country, conn):
    
    # check types to make sure they are strings and stop injections 
    assert type(email) == str   ,     "email is not valid"
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
    curs.execute("INSERT INTO _user VALUES (%s, %s, %s, %s, %s)", (email, fname, lname, address, city))
    
    conn.commit()
    
    curs.close()
    # conn.close()
    
    print("success")
    
    
def check_search_object(search_object:dict):
    for (_, v) in search_object.items():
        
        if type(v) != str:      return False 
        if not check_field(v):  return False 
        
    return True 
        
    
def new_user_search(search_object, conn):
    assert check_search_object(search_object), "invalid inputs"
    
    # get db conn 
    # conn = psycopg2.connect(dsn.DSN) 
    curs = conn.cursor()
    
    # for simplicity for now, assume we are only accepting vehicles 
    if search_object["search_type"] == "Vehicle":
        to_add = (
            search_object["search_type"],
            search_object["make"],
            search_object["model"],
            search_object["year"], 
            search_object["colour"],
            search_object["type"]
        )
        
        curs.execute("INSERT INTO search_type VALUES (%%, %s, %s, %s, %s, %s, %s)", to_add)
        
    elif search_object["search_type"] == "Bicycle":
        ...
    elif search_object["search_type"] == "Motorcycle":
        ...
        
    conn.commit()
    curs.close()
        
    

def new_scraped_ad(search_object, conn):
    ...


if __name__ == "__main__":
    ...