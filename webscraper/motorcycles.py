import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from geopy.geocoders import Nominatim

# base URL for the Kijiji website
BASE_URL = "https://www.kijiji.ca"

def scrape_motorcycles(num_pages):
    motorcycle_ads = []

    for i in range(num_pages):
        # URL for the first page
        url_to_scrape = BASE_URL + f"/b-motorcycles/canada/page-{i+1}/c30l0"

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
                    motorcycle_ads.append(BASE_URL + l["href"])

    

    # create a dataframe to store our results
    motorcycle_df = pd.DataFrame(columns=["AD URL", "AD ID", "YEAR", "MAKE", "MODEL", "COLOR", "CITY", "COUNTRY"])

    # used for getting City and Country from address string
    geolocator = Nominatim(user_agent="school project")

    for ad_link in (motorcycle_ads):
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
        
        # get year
        try:
            year = soup.find(itemprop="vehicleModelDate").text
        except AttributeError:
            year = ""

        # get make
        try:
            make = soup.find('dt', string='Make').find_next_sibling('dd').text
            print(f"Make: {make}")
        except AttributeError:
            make = ""

        # get model
        try:
            model = soup.find('dt', string='Model').find_next_sibling('dd').text
            print(f"Model: {model}")
            if not model:
                model = "Other"
        except AttributeError:
            model = "Other"

        # get color
        try:
            color = soup.find(itemprop="color").text
            if not color:
                color = "Other"
        except AttributeError:
            color = "Other"

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
                # use googlev3
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
        motorcycle_df = pd.concat([motorcycle_df, pd.DataFrame.from_records([{
            "AD URL": ad_link,
            "AD ID": ad_id,
            "YEAR": year,
            "MAKE": make,
            "MODEL": model,
            "COLOR": color,
            "CITY": city,
            "COUNTRY": country}])],
            ignore_index=True)

    # Cleaning up to make it easier for us
    motorcycle_df = motorcycle_df.reset_index(drop=True)

    return motorcycle_df

# scrape_motorcycles(1)