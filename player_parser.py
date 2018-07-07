# -*- coding: utf-8 -*-
import datetime
import json
import os
import requests
import time
from dao import Dao
from lxml import html

DOMAIN = "https://sofifa.com/"
HEADERS = {'User-Agent': 'Mozilla/5.0'}

def parse_player_data(player_id):
    url  = DOMAIN + "player/" + str(player_id)
    print(url)

    response = requests.get(url, headers = HEADERS)
    content = html.fromstring(response.text)

    # short_name, full_name, position, nationality
    player = content.xpath('//div[@class="player"]')[0]
    info = player.xpath('//div[@class="info"]')[0]
    short_name = info.xpath('//h1')[0].text_content().split(' (')[0]
    meta = info.xpath('//div[@class="meta"]/span')[0].text_content()
    full_name = meta.split('Age ')[0].split('  ')[0]
    position = meta.split('Age ')[0].split('  ')[1]
    position = position.replace(' ', ',')
    nationality = info.xpath('//div[@class="meta"]/span/a')[0].attrib['href']
    nationality = nationality.split('=')[1]

    # birthday, height, weight
    data = meta.split('Age ')[1]
    data = data.split(') ')
    birthday = data[0].split('(')[1]
    birthday = datetime.datetime.strptime(birthday, '%b %d, %Y')
    birthday = birthday.strftime('%Y%m%d')
    data = data[1].split(' ')
    height = data[0].replace("cm", "")
    weight = data[1].replace("kg", "")

    # foot
    teams = player.xpath('//div[@class="teams"]')[0]
    data = teams.xpath('//ul[@class="pl"]/li')[0].text_content()
    foot = data.split("\n")[2][:1]

    return (
        player_id, 
        full_name, short_name, birthday, nationality, position, height, weight, foot, 
        full_name, short_name, birthday, nationality, position, height, weight, foot
    )

def parse_rating_data(player_id):
    url  = DOMAIN + "player/" + str(player_id) + "/changeLog"

    response = requests.get(url, headers = HEADERS)
    content = html.fromstring(response.text)

    # rating
    table = content.xpath('//table[@class="table"]')[0]
    rating = table.xpath('//td[@class="text-clip"]/span')[0].text_content() 

    today = time.strftime('%Y%m%d', time.localtime(time.time()))

    rating_record = {}
    rating_record[today] = rating

    # change_log
    index = 0
    change_log = content.xpath('//article[@class="column"]/dl')
    if len(change_log) > 0:
        change_log = change_log[0]
        dt = change_log.xpath('//dt')
        dd = change_log.xpath('//dd')
        for d in dd:
            if "Overall Rating" in d.text_content():
                date = dt[index].text_content()[10:22].strip()
                date = datetime.datetime.strptime(date, '%b %d, %Y')
                date = date.strftime('%Y%m%d')
                
                rating = d.text_content().split('Overall Rating ')[1]
                rating = rating.split('  ')[1].split(' ')[0]
                rating_record[date] = rating.replace('\r\n', '')
            index += 1

    rating_record = json.dumps(convert_rating_data(rating_record))
    return (player_id, rating_record, rating_record)

def convert_rating_data(rating_record):
    temp_year = 1911
    new_year = 1911
    raw_year = 1911
    raw_rating = 0
    max_rating = 0
    rating_set = {}
    for date, rating in sorted(rating_record.items()):
        temp_year = date[:4]
        temp_key = "y" + temp_year
        rating = int(rating)
        if rating > max_rating:
            max_rating = rating

        new_year = int(temp_year)
        if raw_year != 1911:
            if new_year - raw_year > 1:
                for count in range(1, new_year - raw_year):
                    rating_set["y" + str(raw_year + count)] = raw_rating

        if temp_key in rating_set:
            if rating > rating_set[temp_key]:
                rating_set[temp_key] = rating
        else:
            rating_set[temp_key] = rating

        raw_year = int(temp_year)
        raw_rating = rating

    rating_set["max_rating"] = max_rating
    return rating_set

def get_all_player_by_team_id(team_id):
    url  = DOMAIN + "team/" + str(team_id)

    response = requests.get(url, headers = HEADERS)
    content = html.fromstring(response.text)

    player_list = []
    table = content.xpath('//table')[1]
    figure = table.xpath('//figure[@class="avatar"]/img')
    for f in figure:
        player_list.append(int(f.attrib['id']))

    return player_list

"""
Main
"""
if __name__ == "__main__":

    Dao.init()
    Dao.create_sofifa_player()
    Dao.create_sofifa_rating()

    """
    team_id :
     10 = Manchester City,     11 = Manchester United
     18 = Tottenham Hotspur,    9 = Liverpool
      5 = Chelsea,              1 = Arsenal
    241 = Barcelona,          243 = Real Madrid
     45 = Juventus
    """
    player_list = get_all_player_by_team_id(45)
    print(player_list)

    for player_id in player_list:
        player = parse_player_data(player_id)
        rating = parse_rating_data(player_id)
        
        if json.loads(rating[1])["max_rating"] >= 80:
            Dao.upsert_sofifa_player(player)
            Dao.upsert_sofifa_rating(rating)
            print(player)
            print(rating)

        time.sleep(1)