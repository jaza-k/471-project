import psycopg2
from dbfunctions.dsn import DSN
import dbfunctions.insert_data as db_insert
import dbfunctions.dbfuncs as funcs
import webscraper.scraperfuncs as scraper
import pandas as pd 
from time import sleep, time


RUN_MAIN_ROUTINE = True
BASE_URL = "www.kijiji.com"

def reformate_df(df):
    return [dict(row) for _, row in df.iterrows()]  # iterrows is very slow for very large dfs 


def remove_user_active_search(email:str, search_num:int):
    conn = psycopg2.connect(DSN)
    funcs.remove_user_search(email, search_num, conn)
    
    conn.commit()
    conn.close()
    
def schedule_scraping(pages:int, conn):
    
    # scrape vehicles and then add them into the db 
    df_v = scraper.scrape_vehicles(pages)
    inserts_v = reformate_df(df_v)
    for v in inserts_v:
        db_insert.new_scraped_ad(v, "Vehicle", BASE_URL, conn)
    
    # scrape motorcycles and then add them into the db
    df_m = scraper.scrape_motorcycles(pages)
    inserts_m = reformate_df(df_m)
    for m in inserts_m:
        db_insert.new_scraped_ad(m, "Motorcycle", BASE_URL, conn) 
        
        
    conn.commit()
        

def backend_main_subroutine(pages:int, wait_time:int):
    
    conn = psycopg2.connect(DSN)
    
    while RUN_MAIN_ROUTINE:
        
        _start = time()
        schedule_scraping(pages, conn)
        
        funcs.check_matches_against_user_searches(conn)
        _end = time()
        
        seconds_taken = int(_end - _start)
        
        sleep(wait_time - seconds_taken)   # should probably wait ~ 1 hr between scraping and checking new 
        
    conn.commit()
    conn.close()



def test_subroutine_round():
    
    conn = psycopg2.connect(DSN)
    
    schedule_scraping(1, conn) # scrape 1 page for each vehicle and motorcycle and add to db 
    
    curs = conn.cursor()
    test_scrap_q = "SELECT COUNT(*) FROM scraped_ads;"
    
    curs.execute(test_scrap_q)
    result = curs.fetchone()[0]    # should return an int 
    
    print("Number of scraped ads added to the db: ", result) 
    
    curs.close()
    conn.close()
    
    
if __name__ == "__main__":
    
    test_subroutine_round()
    ...
    
    # conn = psycopg2.connect(dsn.DSN)
    # check_matches_against_user_searches(conn)
    # conn.commit()
    
    # conn.close() 