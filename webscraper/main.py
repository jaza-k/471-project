import vehicles
import motorcycles
import pandas as pd

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