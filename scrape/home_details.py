

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

    response = requests.get(URL)
    print(response.status_code)

    #parsed_response = json.load(response.text)
    soup = BeautifulSoup(response.text)
    print(soup.text) #> "\nPlease verify you're a human to continue."
