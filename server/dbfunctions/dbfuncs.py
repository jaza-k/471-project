import psycopg2

def search_matches_found(curs, conn, _matches, usr_search_uuid):

    for m in _matches:
        check_match_exists_q = f"""
        SELECT 
            COUNT(*) 
        FROM 
            matches_with
        WHERE 
            _search_id = '{usr_search_uuid}'
            AND _matched_ad_id = '{m[0]}';
        """

        curs.execute(check_match_exists_q)
        result = curs.fetchone()

        
        # if match isn't already present, insert as new match
        if not result or result[0] == 0:
            insert_matches_q = f"""
            INSERT INTO matches_with (_search_id, _matched_ad_id)
            VALUES ('{usr_search_uuid}', '{m[0]}')"""
            curs.execute(insert_matches_q)
            

def check_matches_against_user_searches(conn):
    # get all user emails 
    curs = conn.cursor()
    email_q = "SELECT u.email FROM _user as u;"
    curs.execute(email_q) 
    emails = curs.fetchall()
    
    # loop over each email and match their searches against what is in the database 
    for _e in emails:
        
        e = _e[0]   # extract the email 
        print("checking: ", e)
        
        
        # get all the users current searches 
        searches_q = """
        SELECT 
            us._sid,
            st._search_type, 
            st._make, 
            st._model, 
            st._year, 
            st._colour, 
            st._body_type 
        FROM 
            search_type as st, 
            user_search as us,
            user_references as ur 
        WHERE 
            us._email = %s AND 
            ur._user_search_id = us._sid AND
            ur._search_uuid = st.__uuid; 
        """
        
        # execute query 
        curs.execute(searches_q, (e,)) 
        
        results = curs.fetchall() 
        
        print("results are: ", results)
        
        # for each active search, search for possible matches 
        for res in results:
            search_uuid = res[0] 
            
            search_ads_q = """
            SELECT 
                sa._ad_id
            FROM 
                search_type as st, 
                scraped_references as sr,
                scraped_ads as sa 
            WHERE 
                st._search_type = %s 
                AND st._make = %s  
                AND (st._model = %s OR st._model = 'Other')
                AND st._year = %s       
                AND (st._colour = %s OR st._colour = 'Other')
                AND (st._body_type = %s OR st._body_type = 'Other')
                AND (sr._ad_uuid = st.__uuid)
                AND (sr._ad_id_origin = sa._ad_id); 
            """
            
            search_ads_params = (res[1], res[2], res[3], res[4], res[5], res[6])
            curs.execute(search_ads_q, search_ads_params)
            
            possible_matches = curs.fetchall()
            print("possible matches: ",possible_matches)
            
            # possible match was found
            if len(possible_matches) > 0:
                search_matches_found(curs, conn, possible_matches, search_uuid)
            
            # else skip to the next 

    conn.commit()
    curs.close()
    
    # end of active search loop 