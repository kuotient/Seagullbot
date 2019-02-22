import json
from bs4 import BeautifulSoup
from riotwatcher import RiotWatcher, ApiError

watcher = RiotWatcher('RGAPI-5bb6c31e-5b70-4e8e-b397-37e46751f363')
my_region = 'KR'
with open('./champions.json', encoding='UTF8') as champions:
    champions = json.load(champions)


def search(name):
    summoner = watcher.summoner.by_name(my_region, name)
    try:
        temp = watcher.spectator.by_summoner(my_region, summoner['id'])
        return 1
    except ApiError as err:
        if err.response.status_code == 404:
            return 0
        else:
            return -1

def find_champion_img(name):
    summoner_info_dict = watcher.summoner.by_name(my_region, name)
    now_playing_dict = watcher.spectator.by_summoner(my_region, summoner_info_dict['id'])

    result = (item for item in now_playing_dict['participants'] if item['summonerName'] == name)
    dict = next(result, False)
    if dict is False:
        return "http://opgg-static.akamaized.net/images/profile_icons/profileIcon27.jpg"
    else:
        key = str(dict['championId'])
        result = (item for item in champions if item['key'] == key)
        dict = next(result, False)
        return dict['icon']

def find_champion_name(name):
    summoner_info_dict = watcher.summoner.by_name(my_region, name)
    now_playing_dict = watcher.spectator.by_summoner(my_region, summoner_info_dict['id'])

    result = (item for item in now_playing_dict['participants'] if item['summonerName'] == name)
    dict = next(result, False)
    if dict is False:
        return "http://opgg-static.akamaized.net/images/profile_icons/profileIcon27.jpg"
    else:
        key = str(dict['championId'])
        result = (item for item in champions if item['key'] == key)
        dict = next(result, False)
        return dict['id']