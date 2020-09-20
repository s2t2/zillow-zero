

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

    address = soup.find("h1", "ds-address-container").text.replace(u'\xa0', u' ') # h/t: https://stackoverflow.com/questions/10993612/how-to-remove-xa0-from-string-in-python
    print("ADDRESS:", address)
