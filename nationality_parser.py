# -*- coding: utf-8 -*-
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
    url = DOMAIN + test
    response = requests.get(url, headers = HEADERS)
    content = html.fromstring(response.text)
    select = content.xpath('//select[@name="na[]"]')[0]
    options = select.xpath('.//option')

    result = {}
    for opt in options:
        key = opt.xpath('.//@value')
        if len(key) > 0:
            result[key[0]] = opt.text_content()

    return result

"""
Main
"""
if __name__ == "__main__":

    Dao.init()
    Dao.create_sofifa_nationality()

    time_node = get_all_time_node()
    nationality = get_all_nationality(time_node)
    print(nationality)