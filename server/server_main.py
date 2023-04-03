
import psycopg2
import insert_data
import webscraper.main as scraper
import pandas as pd


def reformate_df(df):
    return [dict(row) for _, row in df.iterrows()] # iterrows is very slow for very large dfs 

def schedule_scrape():
    vehicles = scraper.scrape_vehicles()

def search_matches_found(curs, _matches, usr_search_uuid):

    for m in _matches:
        check_match_exists_q = f"""SELECT COUNT(*) FROM matches_with
WHERE _search_id = '{usr_search_uuid}'
AND _matched_ad_id = '{m[0]}';"""

        curs.execute(check_match_exists_q)
        result = curs.fetchall()

        # if match isn't already present, insert as new match
        if not result or len(result) <= 0:
            insert_matches_q = f"""INSERT INTO matches_with (_search_id, _matched_ad_id)
VALUES ('{usr_search_uuid}', '{m[0]}');"""
            curs.execute(insert_matches_q)



def check_matches_against_user_searches(conn):
    # get all user emails 
    curs = conn.cursor()
    email_q = "SELECT u.email FROM _user;"
    curs.execute(email_q) 
    emails = curs.fetchall()
    
    # loop over each email and match their searches against what is in the database 
    for _e in emails:
        
        e = _e[0]   # extract the email 
        
        # get all the users current searches 
        searches_q = """
        SELECT 
            st.__uuid
            st._search_type, 
            st._make, 
            st._model, 
            st._year, 
            st._colour, 
            st._body_type 
        FROM 
            search_type as st, 
            user_search as us 
        WHERE 
            us.email = %s AND us._sid = st.__uuid; 
        """
        
        # execute query 
        curs.execute(searches_q, (e,)) 
        
        results = curs.fetchall() 
        
        # for each active search, search for possible matches 
        for res in results:
            search_uuid = res[0] 
            
            search_ads_q = """
            SELECT 
                st.__uuid,
                st._search_type, 
                st._make, 
                st._model, 
                st._year, 
                st._colour, 
                st._body_type 
            FROM 
                search_type as st, 
            WHERE 
                st._seach_type = %s 
                AND st._make = %s  
                AND (st._model = %s OR st._model = 'Other')
                AND st._year = %s       
                AND (st._colour = %s OR st._colour = 'Other')
                AND (st._body_type = %s OR st._body_type = 'Other')
                AND st.__uuid NOT IN (
                    SELECT 
                        st.__uuid 
                    FROM 
                        search_type as st, 
                        user_search as us
                    WHERE 
                        us._sid != st.__uuid
                    );
            """
            
            search_ads_params = (res[1], res[2], res[3], res[4], res[5], res[6])
            curs.execute(search_ads_q, search_ads_params)
            
            possible_matches = curs.fetchall()
            
            # possible match was found
            if len(possible_matches) > 0:
                search_matches_found(curs, possible_matches, search_uuid)
            
            # else skip to the next 

    conn.commit()
    curs.close()
    
    # end of active search loop 
    
if __name__ == "__main__":
    ... 