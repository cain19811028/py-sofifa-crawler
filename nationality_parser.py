import datetime
import json
import os
import requests
import time
from dao import Dao
from lxml import html

DOMAIN = "https://sofifa.com"
HEADERS = {'User-Agent': 'Mozilla/5.0'}

def get_all_time_node():
    response = requests.get(DOMAIN, headers = HEADERS)
    content = html.fromstring(response.text)
    time_node = content.xpath('//div[@class="card-body"]/a/@href')
    return time_node

def get_all_nationality(time_node):
    test = time_node[0]
    print(test)
    url = DOMAIN + test
    response = requests.get(url, headers = HEADERS)
    content = html.fromstring(response.text)
    print(content.text_content())
    nationality_list = []
    return nationality_list

"""
Main
"""
if __name__ == "__main__":

    Dao.init()
    Dao.create_sofifa_nationality()

    time_node = get_all_time_node()
    nationality_list = get_all_nationality(time_node)
    print(nationality_list)