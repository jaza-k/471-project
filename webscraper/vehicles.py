import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from geopy.geocoders import Nominatim

# base URL for the Kijiji website
BASE_URL = "https://www.kijiji.ca"

def scrape_vehicles(num_pages):
    vehicle_ads = []

    for i in range(num_pages):
        # URL for the first page
        url_to_scrape = BASE_URL + f"/b-cars-trucks/canada/used/page-{i+1}/c174l0a49"

        options = webdriver.FirefoxOptions()
        options.add_argument("--headless")
        browser = webdriver.Firefox(options=options)
        browser.get(url_to_scrape)
        html = browser.page_source

        # use BS to parse the text of the HTML response
        soup = BeautifulSoup(html, 'lxml')

        # find all of the relevant ads
        ads = soup.find_all("div", attrs={"class": ["search-item", "regular-ad"]})

        # removes marketing / third party ads
        ads = [x for x in ads if ("cas-channel" not in x["class"]) & ("third-party" not in x["class"])]

        # create a list to store all of the URLs from the 
        for ad in ads:
            # parse the link from the ad
            link = ad.find_all("a", {"class": "title"})
            # add the link to the list, if its not kijiji autos
            for l in link:
                if ("kijijiautos.ca" not in l["href"]):
                    vehicle_ads.append(BASE_URL + l["href"])

    # create a dataframe to store our results
    vehicle_df = pd.DataFrame(columns=["AD URL", "AD ID", "YEAR", "MAKE", "MODEL", "COLOR", "BODY TYPE", "CITY", "COUNTRY"])

    # used for getting City and Country from address string
    geolocator = Nominatim(user_agent="school project")

    for ad_link in (vehicle_ads):
        # grab webpage information & transform with BS
        browser.get(ad_link)
        html = browser.page_source
        soup = BeautifulSoup(html, "lxml")

        ad_id = year = make = model = color = body_type = city = country = None

        # get Ad ID
        try:
            ad_id = ad_link.split("/")[-1].replace("m", "")
        except AttributeError:
            ad_id = ""
        
        # get vehicle year
        try:
            year = soup.find(itemprop="vehicleModelDate").text
        except AttributeError:
            year = ""

        # get vehicle make
        try:
            make = soup.find(itemprop="brand").text
        except AttributeError:
            make = ""

        # get vehicle model
        try:
            model = soup.find(itemprop="model").text
            if not model:
                model = "Other"
        except AttributeError:
            model = "Other"

        # get vehicle color
        try:
            color = soup.find(itemprop="color").text
            if not color:
                color = "Other"
        except AttributeError:
            color = "Other"

        # get vehicle body type
        try:
            body_type = soup.find(itemprop="bodyType").text
            if not body_type:
                body_type = "Other"
        except AttributeError:
            body_type = "Other"

        # get address
        # its free but messy lol
        try:
            address = soup.find(itemprop="address").text
            location = geolocator.geocode(address, addressdetails=True)

            if "city" in location.raw["address"]:
                city = location.raw["address"]["city"].lower()
            elif "village" in location.raw["address"]:
                city = location.raw["address"]["village"].lower()
            elif "town" in location.raw["address"]:
                city = location.raw["address"]["town"].lower()
            else:
                city = ad_link.split("/")[4]

            # if not location:
                # use googlev3?
        except AttributeError:
            city = ad_link.split("/")[4]

        # some of what I've noticed that can be replaced
        city = city.replace("ville-de-", "")
        city = city.replace("city-of-", "")
        city = city.replace("city of ", "")
        city = city.replace("-", " ")
        city = city.replace("(old)", "")

        # Maybe we change this? It would also be a janky solution tho and all we scrape is canada right now anyways
        country = "Canada"

        # apend information to the dataframe
        vehicle_df = pd.concat([vehicle_df, pd.DataFrame.from_records([{
            "AD URL": ad_link,
            "AD ID": ad_id,
            "YEAR": year,
            "MAKE": make,
            "MODEL": model,
            "COLOR": color,
            "BODY TYPE": body_type,
            "CITY": city,
            "COUNTRY": country}])],
            ignore_index=True)

    # Cleaning up to make it easier for us
    vehicle_df['BODY TYPE'].replace('SUV, Crossover','SUV',inplace=True)
    vehicle_df['BODY TYPE'].replace('Coupe (2 door)','Coupe',inplace=True)
    vehicle_df['BODY TYPE'].replace('Minivan, Van','Van',inplace=True)
    vehicle_df['BODY TYPE'].replace('Wagon','Hatchback',inplace=True) # wagon and hatchback are basically the same, for our use case lol
    vehicle_df['BODY TYPE'].replace('Pickup Truck','Truck',inplace=True)
    vehicle_df = vehicle_df.reset_index(drop=True)

    return vehicle_df

# scrape_vehicles(1)