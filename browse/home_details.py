

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
    # options = webdriver.ChromeOptions()
    # options.add_argument('--incognito')
    # options.add_argument('--headless')
    # driver = webdriver.Chrome(CHROMEDRIVER_PATH, chrome_options=options)

    driver.get(HOME_URL)
    print(driver.title) #>
    driver.save_screenshot(os.path.join(os.path.dirname(__file__), "..", "img", "screenshots", "home_details.png"))

    soup = BeautifulSoup(driver.page_source, features="html.parser")

    address = soup.find("h1", "ds-address-container").text
    print("ADDRESS:", clean_str(address))

    price = soup.find("h3", "ds-price").text
    print("LIST PRICE:", clean_str(price))

    #details = soup.find("h3", "ds-bed-bath-living-area-container").text
    #print("DETAILS STR  ", clean_str(details))
    #beds = details.split(" | ")
    #baths =
    #sqft =

    details = soup.find("h3", "ds-bed-bath-living-area-container").find_all("span", "ds-bed-bath-living-area")
    details = [d.text for d in details] #> ['1 bd', '1 ba', '788 Square Feet']
    #bd, ba, sqft = details
    bd = int([detail.replace(" bd", "") for detail in details if "bd" in detail][0])
    ba = int([detail.replace(" ba", "") for detail in details if "ba" in detail][0])
    sqft = int([detail.replace(" Square Feet", "") for detail in details if "Square Feet" in detail][0])
