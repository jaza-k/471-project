import dsn 
import psycopg2
import server_main 



def test_checking_matches():
    conn = psycopg2.connect(dsn.DSN)
    
    server_main.check_matches_against_user_searches(conn)
    
    
    conn.commit()
    conn.close()


if __name__ == "__main__":
    test_checking_matches()