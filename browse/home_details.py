

import os
#import json

from dotenv import load_dotenv
#import requests
from selenium import webdriver
#from selenium.webdriver import Chrome
#from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from pandas import DataFrame

load_dotenv()

CHROMEDRIVER_PATH = os.getenv("CHROMEDRIVER_PATH", default="/usr/local/bin/chromedriver") # get yours with `which chromedriver`
HOME_URL = os.getenv("HOME_URL") # https://www.zillow.com/homedetails/<ADDRESS-TEXT>/<ZPID>_zpid/

def clean_str(mystr):
    # h/t: https://stackoverflow.com/questions/10993612/how-to-remove-xa0-from-string-in-python
    return mystr.replace(u'\xa0', u' ')

if __name__ == "__main__":

    print("HOME URL:", HOME_URL)
    #print("CHROME DRIVER:", CHROMEDRIVER_PATH)

    driver = webdriver.Chrome(CHROMEDRIVER_PATH)
    # ... OR IN "HEADLESS MODE"...
    #options = webdriver.ChromeOptions()
    #options.add_argument('--incognito')
    #options.add_argument('--headless')
    #driver = webdriver.Chrome(CHROMEDRIVER_PATH, options=options)

    driver.get(HOME_URL)
    print("PAGE TITLE:", driver.title)
    driver.save_screenshot(os.path.join(os.path.dirname(__file__), "..", "img", "screenshots", "home_details.png"))

    soup = BeautifulSoup(driver.page_source, features="html.parser")

    try:

        address = soup.find("h1", "ds-address-container").text
        print("ADDRESS:", clean_str(address))

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

        breakpoint()

    finally:
        driver.quit()
