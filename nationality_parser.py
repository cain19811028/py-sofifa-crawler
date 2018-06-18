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

    return content.xpath('//div[@class="card-body"]/a/@href')

def get_all_nationality(time_node):
    
    index = 1
    result = {}
    print("time node count : " + str(len(time_node)))
    
    for link in time_node:
        url = DOMAIN + link
        print(str(index) + ". " + url)
        response = requests.get(url, headers = HEADERS)
        content = html.fromstring(response.text)
        select = content.xpath('//select[@name="na[]"]')[0]
        options = select.xpath('.//option')

        for opt in options:
            key = opt.xpath('.//@value')
            if len(key) > 0:
                result[key[0]] = opt.text_content()

        index += 1
        time.sleep(1)

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

    for k, v in nationality.items():
        Dao.upsert_nationality((k, v, v ))