import requests
from lxml import html

DOMAIN = "https://sofifa.com/"
HEADERS = {'User-Agent': 'Mozilla/5.0'}

def parse_player_data(player_id):
    url  = DOMAIN + "player/" + str(player_id)
    print(url)

    response = requests.get(url, headers = HEADERS)
    content = html.fromstring(response.text)
    print(content)

"""
Main
"""
PLAYER_SET = [158023]

for player_id in PLAYER_SET:
    parse_player_data(player_id)