import datetime
import requests
import time
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
    position = position.split(' ')
    nationality = info.xpath('//div[@class="meta"]/span/a')[0].attrib['href']
    nationality = nationality.split('=')[1]
    print(short_name)
    print(full_name)
    print(position)
    print(nationality)

    # birthday, height, weight
    data = meta.split('Age ')[1]
    data = data.split(') ')
    birthday = data[0].split('(')[1]
    birthday = time.mktime(time.strptime(birthday, '%b %d, %Y'))
    birthday = time.strftime("%Y%m%d", time.gmtime(birthday))
    data = data[1].split(' ')
    height = data[0].replace("cm", "")
    weight = data[1].replace("kg", "")
    print(birthday)
    print(height)
    print(weight)

    # foot
    teams = player.xpath('//div[@class="teams"]')[0]
    data = teams.xpath('//ul[@class="pl"]/li')[0].text_content()
    foot = data.split("\n")[2][:1]
    print(foot)

def parse_rating_data(player_id):
    url  = DOMAIN + "player/" + str(player_id) + "/changeLog"
    print(url)

    response = requests.get(url, headers = HEADERS)
    content = html.fromstring(response.text)

    # rating
    table = content.xpath('//table[@class="table"]')[0]
    rating = table.xpath('//td[@class="text-clip"]/span')[0].text_content() 

    today = time.strftime('%Y%m%d',time.localtime(time.time()))

    rating_record = {}
    rating_record[today] = rating
    print(rating_record)

    # change_log
    index = 0
    change_log = content.xpath('//article[@class="column"]/dl')[0]
    dt = change_log.xpath('//dt')
    dd = change_log.xpath('//dd')
    for d in dd:
        if "Overall Rating" in d.text_content():
            date = dt[index].text_content()[10:22]
            print(date)
            print(d.text_content())
        index += 1

"""
Main
"""
if __name__ == "__main__":
    
    PLAYER_SET = [158023]

    for player_id in PLAYER_SET:
        # parse_player_data(player_id)
        parse_rating_data(player_id)