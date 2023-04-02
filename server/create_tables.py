import psycopg2 
import postgres_tables
from dsn import DSN


# resoruces 
# https://www.psycopg.org/docs/connection.html


def drop_all_tables(conn):
    curs = conn.cursor()
    
    print("dropping tables first")
    
    drop_query = "DROP TABLE IF EXISTS " + ", ".join(postgres_tables.TABLE_NAMES) + ";"
    
    print("dropping tables successful")
    
    curs.execute(drop_query)
    conn.commit()

def create_postgres_tables(conn):
    
    curs = conn.cursor()
    for (i, table_query) in enumerate(postgres_tables.TABLES_CREATE_QUERIES):
        
        print(f"table {i} from the list to be executed")
        
        curs.execute(table_query)
        
        print(f"table {i} from the list has been successfully made")
        
        conn.commit()

if __name__ == "__main__":
    conn = psycopg2.connect(DSN)
    
    # drop_all_tables(conn)
    # create_postgres_tables(conn)
    # df = pd.DataFrame([])
    # str_df = df.to_string()
    # print(str_df)
    
    conn.close()
    
            
    