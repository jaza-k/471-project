import vehicles
import motorcycles
import pandas as pd
import pickle


def scrape_vehicles(num_of_pages:int):
    vehicles_df = vehicles.scrape_vehicles(num_of_pages)
    return vehicles_df 

def scrape_motorcycles(num_of_pages:int):
    motorcycles_df = motorcycles.scrape_motorcycles(num_of_pages)
    return motorcycles_df

def scrape():
    vehicles_df = vehicles.scrape_vehicles(1)
    motorcycles_df = motorcycles.scrape_motorcycles(1)
    #would be the same sort of format for bikes and motorcycles

    #insert to database here?

def search_for_matches():
    print("Searching for matches")
    # activate database queries
    # probably happens when a user submits a new search? or timed?

def insert_user_data():
    print("inserting user data")

def notify_user():
    print("Email sent to user")
    
    
def save_sample_vehicle():
    df = scrape_vehicles(1) 
    to_pickle = [dict(row) for _, row in df.iterrows()]
    with open('vehicle_sample.pickle', 'wb') as f:
        pickle.dump(to_pickle, f)
        
def save_sample_motorcycle():
    df = scrape_motorcycles(1) 
    to_pickle = [dict(row) for _, row in df.iterrows()]
    with open('motorcycle_sample.pickle', 'wb') as f:
        pickle.dump(to_pickle, f)
        
        
        
if __name__ == "__main__":
    save_sample_vehicle()
    save_sample_motorcycle()