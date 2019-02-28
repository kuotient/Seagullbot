import json
from bs4 import BeautifulSoup
from riotwatcher import RiotWatcher, ApiError
import configparser


config = configparser.ConfigParser()
config.read('./options.ini')

RIOT_TOKEN = config['DEFAULT']['RIOT_TOKEN']

watcher = RiotWatcher(RIOT_TOKEN) # 갱신 필요.
my_region = 'KR'
with open('./data/champions.json', encoding='UTF8') as champions:
    champions = json.load(champions)


async def search_stats(argv, argc, client, message):
    if argc == 1:
        searching = await client.send_message(message.channel, '아이디를 입력하세요.')
        msg = await client.wait_for_message(timeout=15.0, author=message.author)
        if msg is None:
            await client.delete_message(searching)
            await client.send_message(message.channel, '입력받은 아이디가 없습니다.')
            return

        player_id = msg.content
        await client.delete_message(msg)

        searching = await client.edit_message(searching, '검색중입니다...')
    else:
        player_id = argv[1]
        searching = await client.send_message(message.channel, '검색중입니다...')

    #utils.execute_after(client.send_typing, parameters=message.channel, delay=9)
    await client.send_typing(message.channel)

    summoner = _search(player_id)

    if summoner is None:
        result = '플레이어를 찾을 수 없습니다.'
        await client.send_message(message.channel, result)
        await client.delete_message(searching)
        return

    else:
        result = search_stats(ubisoft_id)
        embed = discord.Embed(title='***:bomb: RAINBOW SIX STATS :bomb:** presented by* r6stats', description=result+"\n**보다 자세한 정보는 [r6stats](https://r6stats.com/stats/" + ubisoft_id + ")**", color=0x879396)
        embed.set_thumbnail(url="https://ubisoft-avatars.akamaized.net/" + ubisoft_id + "/default_256_256.png")
        #embed.set_footer(text=)
        await client.send_message(message.channel, embed=embed)
        await client.delete_message(searching)








def _search(name):
    summoner = watcher.summoner.by_name(my_region, name)
    try:
        temp = watcher.spectator.by_summoner(my_region, summoner['id'])
        return 1
    except ApiError as err:
        if err.response.status_code == 404:
            return None
        else:
            return None

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