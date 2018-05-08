import requests
from lxml import html

DOMAIN = "https://sofifa.com/"
HEADERS = {'User-Agent': 'Mozilla/5.0'}

def parse_player_data(player_id):
    url  = DOMAIN + "player/" + str(player_id)
    print(url)

    response = requests.get(url, headers = HEADERS)
    content = html.fromstring(response.text)

    # name
    temp = content.xpath('//div[@class="player"]')[0]
    temp = temp.xpath('//div[@class="info"]')[0]
    short_name = temp.xpath('//h1')[0].text_content().split(' (')[0]
    full_name = temp.xpath('//div[@class="meta"]/span')[0].text_content()
    full_name = full_name.split('Age ')[0].split('  CF ST RW')[0]
    print(short_name)
    print(full_name)

"""
Main
"""
PLAYER_SET = [158023]

for player_id in PLAYER_SET:
    parse_player_data(player_id)