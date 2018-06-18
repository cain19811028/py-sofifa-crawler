import datetime
import json
import os
import requests
import time
from dao import Dao
from lxml import html

DOMAIN = "https://sofifa.com/"
HEADERS = {'User-Agent': 'Mozilla/5.0'}

def get_all_nationality():
    response = requests.get(DOMAIN, headers = HEADERS)
    content = html.fromstring(response.text)
    nationality_list = []
    return nationality_list

"""
Main
"""
if __name__ == "__main__":

    Dao.init()
    Dao.create_sofifa_nationality()

    nationality_list = get_all_nationality()
    print(nationality_list)