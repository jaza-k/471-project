import insert_data
import psycopg2
import dsn

def test_new_usr():
    fname = "john"
    lname = "smith"
    email = "johnsmith@gmail.com"
    address = "123 fake street"
    city = "calgary"
    country = "Canada"
    
    assert type(email) == str 
    
    fc = insert_data.check_field(email)
    
    print(insert_data.check_field(""))          # should return False 
    print(insert_data.check_field("AzxD"))
    print(insert_data.check_field("aa@4.11222"))
    print(insert_data.check_field("#"))
    
    conn = psycopg2.connect(dsn.DSN)
    
    insert_data.new_user_info(email, fname, lname, address, city, country)
    
    curs = conn.cursor()
    q = f"SELECT * FROM _user;"
    curs.execute(q) 
    res = curs.fetchone()
    
    print(f"got back: {res}")
    
    
def test_new_usr_search():
    search_object = {
        "search_type": "Vehicle",
        "make" : "yes",
        "model" : "123",
        "year" : "1997", 
        "colour" : "blue",
        "body_type" : "yes"
    }
    
    email = "johnsmith@gmail.com"
    _city = "calgary"
    
    insert_data.new_user_search(search_object, email, _city)
    
    conn = psycopg2.connect(dsn.DSN)
    curs = conn.cursor()
    q = f"SELECT * FROM user_search;"
    curs.execute(q) 
    res = curs.fetchone()
    
    print(f"got back: {res}")
    
    q = "SELECT * FROM search_type;"
    curs.execute(q) 
    res = curs.fetchone()
    
    print(f"got back: {res}")

if __name__ == "__main__":
    # test_new_usr()
    test_new_usr_search()