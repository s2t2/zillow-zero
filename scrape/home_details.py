

import os
#import json

from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
from pandas import DataFrame

load_dotenv()

URL = os.getenv("HOME_URL") # like

#class HomePageScraper:
#    def __init__(self, url=URL):
#       self.url = url

if __name__ == "__main__":

    print("HOME URL:", URL)
    #response = requests.get(URL)
    #print(response.status_code)
    #soup = BeautifulSoup(response.text)
    #print(soup.text) #> "\nPlease verify you're a human to continue."

    with requests.Session() as session:
        response = session.get(URL, headers={
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.8',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
        })
        print(response.status_code)

        soup = BeautifulSoup(response.text, features="html.parser")
        print(soup.text) #> "\nPlease verify you're a human to continue."


        breakpoint()

        address = soup.find("h1", "ds-address-container").text
        print("ADDRESS:", address)

        price = soup.find("h3", "ds-price").text
        print("LIST PRICE:", price)
        price = int(price.replace("$","").replace(",",""))

        details = soup.find("h3", "ds-bed-bath-living-area-container").find_all("span", "ds-bed-bath-living-area")
        details = [d.text for d in details] #> ['1 bd', '1 ba', '123 Square Feet']
        #print(details)
        bd = int([detail.replace(" bd", "") for detail in details if "bd" in detail][0])
        ba = int([detail.replace(" ba", "") for detail in details if "ba" in detail][0])
        sqft = int([detail.replace(" Square Feet", "") for detail in details if "Square Feet" in detail][0])
        print("DETAILS:", bd, "BD", ba, "BA |", sqft, "SQFT")

        status = soup.find("span", "ds-status-details").text
        print("STATUS:", status) #> 'Contingent'

        #z_price = soup.find("div", "ds-chip-removable-content").text
        #z_price = int(z_price.strip().split("$")[1].replace(",", ""))
        #print("Z PRICE", z_price)

        # to get full desc, need to first click the "Read more" button in the "ds-overview-section"
        desc = soup.find("div", "ds-overview-section").text
        print("DESCRIPTION:", desc)

        facts = soup.find("ul", "ds-home-fact-list").find_all("li", "ds-home-fact-list-item")
        home_type = [fact.text.replace("Type:","") for fact in facts if "Type:" in fact.text][0]
        year_built = int([fact.text.replace("Year built:","") for fact in facts if "Year built:" in fact.text][0])
        heating = [fact.text.replace("Heating:","") for fact in facts if "Heating:" in fact.text][0]
        cooling = [fact.text.replace("Cooling:","") for fact in facts if "Cooling:" in fact.text][0]
        parking = [fact.text.replace("Parking:","") for fact in facts if "Parking:" in fact.text][0]
        hoa = int([fact.text.split("$")[1].split("/")[0] for fact in facts if "HOA:" in fact.text][0])
        ppsqft = int([fact.text.replace("Price/sqft:","").replace("$","") for fact in facts if "Price/sqft:" in fact.text][0])
        print("HOME TYPE:", home_type)
        print("YEAR BUILT:", year_built)
        print("HEATING:", heating, "COOLING:", cooling)
        print("PARKING:", parking)
        print("HOA:", hoa)
        print("PRICE PER SQFT:", ppsqft)
