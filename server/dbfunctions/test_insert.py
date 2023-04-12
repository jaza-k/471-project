import insert_data
import psycopg2
import dsn
import pickle 
from postgres_tables import TABLE_NAMES

def clear_tables():
    conn = psycopg2.connect(dsn.DSN)
    curs = conn.cursor()
    
    _tables = TABLE_NAMES
    
    
    
    tables = ", ".join(_tables)
    q = ""
    # remove all constraints for the foreign keys 
    for t in _tables:
        q += "ALTER TABLE " + t + " DISABLE TRIGGER ALL;\n"
        # curs.execute(q)
   
    # q = f"TRUNCATE TABLE {tables} CASCADE;"
    # curs.execute(q)
    
    for t in _tables:
        q += "DELETE FROM " + t + ";\n"
        # curs.execute(q)
    
    # re-add all constraints for the foreign keys 
    for t in _tables:
        q += "ALTER TABLE "+ t + " ENABLE TRIGGER ALL;\n"
        # curs.execute(q)
    
    # print(q)
    
    curs.execute(q)
    conn.commit()
    
    print("all tables cleared")

def test_new_usr():
    fname = "john"
    lname = "smith"
    email = "petermichaelkuchel@gmail.com"
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
    
    insert_data.new_user_info(email, fname, lname, address, city, country, conn)
    
    curs = conn.cursor()
    q = f"SELECT * FROM _user;"
    curs.execute(q) 
    res = curs.fetchone()
    
    print(f"got back: {res}")
    
    
def test_new_usr_search():
    search_object = {
        "search_type": "Vehicle",
        "make" : "Dodge",
        "model" : "Journey",
        "year" : "2011", 
        "colour" : "Blue",
        "body_type" : "SUV"
    }
    
    email = "petermichaelkuchel@gmail.com"
    _city = "calgary"
    
    
    
    conn = psycopg2.connect(dsn.DSN)
    
    insert_data.new_user_search(search_object, email, _city, conn)
    
    curs = conn.cursor()
    q = f"SELECT * FROM user_search;"
    curs.execute(q) 
    res = curs.fetchone()
    
    print(f"got back: {res}")
    
    q = "SELECT * FROM search_type;"
    curs.execute(q) 
    res = curs.fetchone()
    
    print(f"got back: {res}")

def get_pickle(_file):
    with open(_file, 'rb') as f:
        return pickle.load(f)
    
def test_ad_single_insertion():
    v = get_pickle("/home/ubuntu/471-project/vehicle_sample.pickle")
    # m = get_pickle("/home/ubuntu/471-project/motorcycle_sample.pickle")
    # print(v)
    conn = psycopg2.connect(dsn.DSN)
    curs = conn.cursor()
    
    marketplace = "https://www.kijiji.ca"
    ad_type = "Vehicle"
    v0 = v[0]    
    
    q1 = "SELECT * FROM scraped_ads;"
    curs.execute(q1)
    res = curs.fetchone()
    print("got back before: ", res)
    
    insert_data.new_scraped_ad(v0, ad_type, marketplace)     

    
    
    q1 = "SELECT * FROM scraped_ads;"
    curs.execute(q1)
    res = curs.fetchone()
    print("got back: ", res)
    
    
    curs.close()
    conn.close()    
    
def test_ads_multi_insertions():
    vs = get_pickle("/home/ubuntu/471-project/vehicle_sample.pickle")
    # for v in vs:
    #     print(v)
    #     print("\n")
    conn = psycopg2.connect(dsn.DSN)
    curs = conn.cursor()
    
    marketplace = "https://www.kijiji.ca"
    ad_type = "Vehicle"
    
    for v in vs:
        # q1 = "SELECT * FROM scraped_ads;"
        # curs.execute(q1)
        # res = curs.fetchall()
        # print("count before insertion: ", len(res))
        
        insert_data.new_scraped_ad(v, ad_type, marketplace, conn)
        
        # q1 = "SELECT * FROM scraped_ads;"
        # curs.execute(q1)
        # res = curs.fetchall()
        # print("count after insertion: ", len(res))
    
    conn.commit()
    curs.close()
    
    conn.close()  
        
        
    
    
    
    
    
if __name__ == "__main__":
    clear_tables()
    test_new_usr()
    test_new_usr_search()
    test_ads_multi_insertions()