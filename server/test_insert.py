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
    
    insert_data.new_user_info(email, fname, lname, address, city, country, conn)
    
    curs = conn.cursor()
    q = f"SELECT * FROM _user;"
    curs.execute(q) 
    res = curs.fetchone()
    
    print(f"got back: {res}")
    
    
    

if __name__ == "__main__":
    test_new_usr()