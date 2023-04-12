import psycopg2
from datetime import datetime
from emails import send_email

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
            
            # send the user an email 
            get_usr = """
            "SELECT 
                us.email, 
                ur.name 
            FROM 
                user_search as us, 
                _user as ur 
            WHERE 
                us._sid = %s AND
                us._email = ur.email; 
            """
            
            curs.execute(get_usr, (usr_search_uuid,)) 
            res = curs.fetchone()
            email, fname = res 
            
            # send the user an email to let them know
            # it should only eamil them once since if the possible match is 
            # already in the db then it won't send it again
            send_email.send_email_notification(email, fname) 
            
            
            

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
    
    
def remove_user_search(email:str, search_number:int, conn):
    
    # conn = psycopg2.connect(dsn.DSN)
    curs = conn.cursor()
    
    user_search_q = f"""
    SELECT 
        us._sid
    FROM 
        user_search as us
    WHERE 
        us._email = '{email}' AND 
        us._usr_search_num = '{search_number}'; 
    """
    
    curs.execute(user_search_q)
    us_id = curs.fetchone()[0]        # fetch the user_search id 
    
    # add it to the history table 
    current_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    insert_history = "INSERT INTO history_table VALUES (%s, %s, %s)"
    
    curs.execute(insert_history, (us_id, email, current_time)) 
    
    """
    remove user search from the tables that it appears in 
    
    should still be able to retrieve the information from the 
    user_references table if needed, and in the search_type table will still have the 
    information that the user entered in
    """
    delete_query = """
    
    DELETE FROM user_search WHERE _sid = '{us_id}';
    DELETE FROM matches_with WHERE _search_id = '{us_id}';
    """
    
    curs.execute(delete_query)
    
    conn.commit()
    curs.close()