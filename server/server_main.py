import psycopg2
import dbfunctions.dsn as dsn
import dbfunctions.insert_data as db_insert
import dbfunctions.dbfuncs as funcs
import webscraper.scraperfuncs as scraper
import pandas as pd 
from time import sleep, time


RUN_MAIN_ROUTINE = True
BASE_URL = "www.kijiji.com"

def reformate_df(df):
    return [dict(row) for _, row in df.iterrows()]  # iterrows is very slow for very large dfs 


def remove_user_search(email:str, search_number:int):
    ...


def schedule_scraping(pages:int):
    
    # scrape vehicles and then add them into the db 
    df_v = scraper.scrape_vehicles(pages)
    inserts_v = reformate_df(df_v)
    for v in inserts_v:
        db_insert.new_scraped_ad(v, "Vehicle", BASE_URL)
    
    # scrape motorcycles and then add them into the db
    df_m = scraper.scrape_motorcycles(pages)
    inserts_m = reformate_df(df_m)
    for m in inserts_m:
        db_insert.new_scraped_ad(m, "Motorcycle", BASE_URL) 
        

def backend_main_subroutine(pages:int, wait_time:int):
    
    conn = psycopg2.connect(dsn.DSN)
    
    while RUN_MAIN_ROUTINE:
        
        _start = time()
        schedule_scraping()
        
        funcs.check_matches_against_user_searches(conn)
        _end = time()
        
        seconds_taken = int(_end - _start)
        
        sleep(wait_time - seconds_taken)   # should probably wait ~ 1 hr between scraping and checking new 
        
    conn.commit()
    conn.close()
        
if __name__ == "__main__":
    ...
    # conn = psycopg2.connect(dsn.DSN)
    # check_matches_against_user_searches(conn)
    # conn.commit()
    
    # conn.close() 