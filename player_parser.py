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
    url  = DOMAIN + "player/" + str(player_id) + "?units=mks"
    print(url)

    response = requests.get(url, headers = HEADERS)
    content = html.fromstring(response.text)

    # short_name, full_name, position, nationality
    player = content.xpath('//div[@class="player"]')[0]
    info = player.xpath('//div[@class="info"]')[0]
    short_name = info.xpath('//h1')[0].text_content().split('(ID')[0]
    meta = info.xpath('//div[@class="meta"]')[0].text_content()
    full_name = meta.split('Age ')[0].split('  ')[0]
    position = meta.split('Age ')[0].split('  ')[1]
    position = position.replace(' ', ',')
    nationality = info.xpath('//div[@class="meta"]/a')[0].attrib['href']
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
    card = player.xpath('.//div')[8]
    data = card.xpath('//ul[@class="pl"]/li')[0].text_content()
    foot = data.replace('Preferred Foot', '').strip()[:1]

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
                date = dt[index].text_content()[-14:].strip()
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
        temp_key = str(temp_year)
        rating = int(rating)
        if rating > max_rating:
            max_rating = rating

        new_year = int(temp_year)
        if raw_year != 1911:
            if new_year - raw_year > 1:
                for count in range(1, new_year - raw_year):
                    rating_set[str(raw_year + count)] = raw_rating

        if temp_key in rating_set:
            if rating > rating_set[temp_key]:
                rating_set[temp_key] = rating
        else:
            rating_set[temp_key] = rating

        raw_year = int(temp_year)
        raw_rating = rating

    rating_set["max_rating"] = max_rating
    return rating_set

def get_player_by_team_id(team_id):
    url  = DOMAIN + "team/" + str(team_id)

    response = requests.get(url, headers = HEADERS)
    content = html.fromstring(response.text)

    player_set = []
    table = content.xpath('//table')
    table = table[1] if len(table) > 1 else table[0]
    figure = table.xpath('//figure[@class="avatar"]/img')
    
    for f in figure:
        player_set.append(int(f.attrib['id']))

    return player_set

def get_all_time_player_by_team_id(team_id):

    index = 1
    time_node = get_all_time_node()
    print("time node count : " + str(len(time_node)))

    player_set = set([])
    for link in time_node:
        url = DOMAIN + "team/" + str(team_id) + link[1:]
        print(str(index) + ". " + url)
        response = requests.get(url, headers = HEADERS)
        content = html.fromstring(response.text)

        table = content.xpath('//table')
        table = table[1] if len(table) > 1 else table[0]
        figure = table.xpath('//figure[@class="avatar"]/img')
        for f in figure:
            player_set.add(int(f.attrib['id']))

        index += 1
        time.sleep(0.1)

    return player_set

def get_all_time_node():

    response = requests.get(DOMAIN, headers = HEADERS)
    content = html.fromstring(response.text)

    return content.xpath('//div[@class="card-body"]/a/@href')

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
    # player_set = get_all_time_player_by_team_id(10)
    # player_set = get_player_by_team_id(10)
    # print("player count : " + str(len(player_set)))
    player_set = {146439, 189963, 186380, 186382, 4111, 186384, 186385, 186386, 225811, 220182, 220185, 210970, 210969, 181786, 13850, 50723, 220198, 218667, 17964, 211501, 198190, 560, 198193, 205362, 181820, 186942, 190531, 20551, 170570, 9805, 229968, 202832, 204884, 233047, 233048, 203864, 163415, 163419, 2651, 168542, 140384, 213089, 183907, 2148, 192613, 137829, 614, 211048, 146536, 164462, 229495, 218744, 231032, 218745, 218746, 237692, 51321, 183427, 153079, 225414, 199304, 211593, 211594, 211595, 51336, 211597, 4233, 201359, 232080, 221329, 175254, 101015, 143001, 221340, 188572, 221342, 221343, 158, 221350, 223912, 183465, 6826, 164009, 138412, 224947, 230068, 224949, 230070, 224951, 24248, 230081, 180930, 230084, 150724, 25798, 141001, 233164, 197837, 52941, 146641, 208594, 212692, 223963, 189668, 5860, 158438, 223977, 223978, 223979, 208622, 189678, 189679, 239, 189682, 189684, 50421, 189686, 189687, 201975, 169721, 212218, 200441, 189691, 189692, 169214, 189693, 216320, 216321, 216322, 186627, 216324, 216325, 2307, 163587, 230666, 185103, 186127, 195858, 215316, 172820, 222492, 221982, 135455, 3363, 50467, 229670, 203574, 139062, 206134, 193848, 53050, 149306, 197948, 171833, 206654, 20289, 134979, 3395, 184134, 53578, 196941, 137551, 210257, 135507, 209750, 229718, 5471, 204639, 229217, 190821, 190822, 183142, 190824, 205161, 205162, 205163, 165740, 183145, 192366, 190823, 119152, 26992, 165239, 235904, 210423, 169718, 205192, 199561, 205193, 1419, 194958, 155539, 222104, 202652, 182696, 169725, 111023, 138671, 199602, 225719, 142784, 450, 139720, 136137, 46027, 232396, 228813, 174543, 136144, 138193, 236499, 192985, 188377, 161754, 39386, 223197, 209886, 199135, 202721, 50660, 227813, 138726, 12265, 152554, 220651, 186345, 220654, 496, 231410, 199159, 210424, 210425, 1533}
    print(player_set)

    for player_id in player_set:
        player = parse_player_data(player_id)
        rating = parse_rating_data(player_id)
        
        if json.loads(rating[1])["max_rating"] >= 80:
            Dao.upsert_sofifa_player(player)
            Dao.upsert_sofifa_rating(rating)
            print(player)
            print(rating)

        time.sleep(0.1)