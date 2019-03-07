import urllib.request
from bs4 import BeautifulSoup
import json
import requests
import discord
import prettytable
from selenium import webdriver
import datetime

PHANTOMJS_PATH = 'phantomjs.exe'

CHROME_PATH = 'chromedriver.exe'


async def siege_search_stats(argc, argv, client, message):
    if argc == 1:
        searching = await client.send_message(message.channel, '아이디를 입력하세요.')
        msg = await client.wait_for_message(timeout=15.0, author=message.author)
        if msg is None:
            await client.delete_message(searching)
            await client.send_message(message.channel, '입력받은 시간 초과입니다.')
            return

        player_id = msg.content
        await client.delete_message(msg)

        searching = await client.edit_message(searching, '검색중입니다...')
    else:
        player_id = argv[1]
        searching = await client.send_message(message.channel, '검색중입니다...')

    ubisoft_id = _search_ubisoft_id(player_id)
    if ubisoft_id.startswith('ERROR:'):
        if ubisoft_id == 'ERROR: timeout':
            result = '현재 데이터베이스 서버 응답이 지연되고 있습니다. 나중에 다시 시도해 주세요.'
        elif ubisoft_id == 'ERROR: internal_server_error':
            result = '데이터베이스 서버에서 에러가 발생하였습니다.'
        else:
            result = '플레이어를 찾을 수 없습니다.'
        await client.send_message(message.channel, result)
        await client.delete_message(searching)
        return

    await client.send_typing(message.channel)
    result = search_stats(ubisoft_id)
    if result.startswith('ERROR:'):
        if result == 'ERROR: timeout':
            embed = discord.Embed(title='***:bomb: RAINBOW SIX STATS :bomb:** presented by* r6stats', description='현재 데이터베이스 서버 응답이 지연되고 있습니다. 나중에 다시 시도해 주세요.'+\
                                                                                                                  "\n**직접 가서 보려면 [r6stats](https://r6stats.com/stats/" + ubisoft_id + ")**", color=0xff0000)
        else:
            embed = discord.Embed(title='***:bomb: RAINBOW SIX STATS :bomb:** presented by* r6stats', description='처리 중 오류가 발생하였습니다.'+\
                                                                                                                  "\n**직접 가서 보려면 [r6stats](https://r6stats.com/stats/" + ubisoft_id + ")**", color=0xff0000)
    else:
        embed = discord.Embed(title='***:bomb: RAINBOW SIX STATS :bomb:** presented by* r6stats', description=result+"\n**보다 자세한 정보는 [r6stats](https://r6stats.com/stats/" + ubisoft_id + ")**", color=0x879396)
        embed.set_thumbnail(url="https://ubisoft-avatars.akamaized.net/" + ubisoft_id + "/default_256_256.png")
    #embed.set_footer(text=)
    await client.send_message(message.channel, embed=embed)
    await client.delete_message(searching)


async def siege_search_operator(argc, argv, client, message):
    if argc == 1:
        searching = await client.send_message(message.channel, '아이디를 입력하세요.')
        msg = await client.wait_for_message(timeout=15.0, author=message.author)
        if msg is None:
            await client.delete_message(searching)
            await client.send_message(message.channel, '입력받은 시간 초과입니다.')
            return

        player_id = msg.content
        await client.delete_message(msg)

        if player_id is None:
            await client.delete_message(searching)
            await client.send_message(message.channel, '입력받은 아이디가 없습니다.')
            return
        searching = await client.edit_message(searching, '검색중입니다..')
    else:
        player_id = argv[1]
        searching = await client.send_message(message.channel, '검색중입니다..')

    ubisoft_id = _search_ubisoft_id(player_id)
    if ubisoft_id.startswith('ERROR:'):
        if ubisoft_id == 'ERROR: timeout':
            result = '현재 데이터베이스 서버 응답이 지연되고 있습니다. 나중에 다시 시도해 주세요.'
        elif ubisoft_id == 'ERROR: internal_server_error':
            result = '데이터베이스 서버에서 에러가 발생하였습니다.'
        else:
            result = '플레이어를 찾을 수 없습니다.'
        await client.send_message(message.channel, result)
        await client.delete_message(searching)
        return

    await client.send_typing(message.channel)
    result, operator_image = search_operator(ubisoft_id)
    if result.startswith('ERROR:'):
        if result == 'ERROR: timeout':
            embed = discord.Embed(title='***:bomb: RAINBOW SIX STATS :bomb:** presented by* r6stats',
                                  description='현재 데이터베이스 서버 응답이 지연되고 있습니다. 나중에 다시 시도해 주세요.' + \
                                              "\n**직접 가서 보려면 [r6stats](https://r6stats.com/stats/" + ubisoft_id + ")**",
                                  color=0xff0000)
        else:
            embed = discord.Embed(title='***:bomb: RAINBOW SIX STATS :bomb:** presented by* r6stats',
                                  description='처리 중 오류가 발생하였습니다.' + \
                                              "\n**직접 가서 보려면 [r6stats](https://r6stats.com/stats/" + ubisoft_id + ")**",
                                  color=0xff0000)
    else:
        embed = discord.Embed(title='***:bomb: RAINBOW SIX STATS :bomb:** presented by* r6stats',
                              description=result + "\n**보다 자세한 정보는 [r6stats](https://r6stats.com/stats/" + ubisoft_id + ")**",
                              color=0x879396)
        embed.set_thumbnail(url=operator_image)

    # embed.set_footer(text=)
    await client.send_message(message.channel, embed=embed)
    await client.delete_message(searching)
    # await client.delete_message(searching)
    # for result in result_list:
    #     await client.send_message(message.channel, result)


def search_stats(ubisoft_id):
    try:
        stat_json = _search(ubisoft_id)
        if 'error' in stat_json:
            if not stat_json['error'].startswith('ERROR:'):
                return 'ERROR: ' + stat_json['error'], None

            return stat_json['error'], None

        overall = stat_json['stats'][0]['general']
        casual = stat_json['stats'][0]['queue']['casual']
        ranked = stat_json['stats'][0]['queue']['ranked']

        message = "**플레이어** : {}\n".format(stat_json['username'])
        message += "**레벨** : {}\n\n".format(stat_json['progression']['level'])
        #message += "**현재 경험치** : {}\n\n".format(stat_json['progression']['total_xp'])

        message += '```'
        message += "".ljust(20) + "총괄".center(13) + "\n\n"
        message += "플레이한 시간".ljust(15) + str(datetime.datetime.fromtimestamp(overall["playtime"]).strftime('%dd %Hh %Mm')).rjust(13) + "\n"
        message += "플레이한 매치".ljust(15) + "{:,}".format(overall["wins"] + overall["losses"]).rjust(13) + "\n"
        message += "매치당 사살 수".ljust(15) + "{0:.2f}".format(overall["kills"] / (overall["wins"] + overall["losses"])).rjust(13) + "\n"
        message += "사살".ljust(18) + "{:,}".format(overall["kills"]).rjust(13) + "\n"
        message += "사망".ljust(18) + "{:,}".format(overall["deaths"]).rjust(13) + "\n"
        message += "킬뎃".ljust(18) + "{0:.2f}".format(overall["kd"]).rjust(13) + "\n"
        message += "승리".ljust(18) + "{:,}".format(overall["wins"]).rjust(13) + "\n"
        message += "패배".ljust(18) + "{:,}".format(overall["losses"]).rjust(13) + "\n"
        message += "승률".ljust(18) + "{0:.2f}".format(overall["wl"]).rjust(13) + "\n"
        message += "눈먼 사살".ljust(16) + "{:,}".format(overall["blind_kills"]).rjust(13) + "\n"
        message += "근접 사살".ljust(16) + "{:,}".format(overall["melee_kills"]).rjust(13) + "\n"
        message += "관통 사살".ljust(16) + "{:,}".format(overall["penetration_kills"]).rjust(13) + "\n"
        message += "헤드샷".ljust(17) + "{:,}".format(overall["headshots"]).rjust(13) + "\n"
        message += "헤드샷 비율".ljust(15) + ("{0:.2f}".format(overall["headshots"] * 100 / overall["kills"]) + "%").rjust(13) + "\n"
        message += "부순 가젯".ljust(16) + "{0:,}".format(overall["gadgets_destroyed"]).rjust(13) + "\n"
        message += "기절시킨 수".ljust(15) + "{0:,}".format(overall["dbnos"]).rjust(13) + "\n"
        message += "소생시킨 수".ljust(15) + "{0:,}".format(overall["revives"]).rjust(13) + "\n"
        #message += "선호 오퍼".rjust(16) + overall["fav_oper"].rjust(13) + "\n\n"
        message += "".ljust(37, '-') + '\n\n'
        message += "".ljust(13) + "캐주얼".center(13) + "랭크".center(13) + "\n\n"
        #message += "|" + "".center(18, '-') + "|" + "".center(13, '-') + "|" + "".center(13, '-') + "|" + "\n"
        message += "사살".ljust(6) + "{:,}".format(casual["kills"]).rjust(16) + "{:,}".format(ranked["kills"]).rjust(14) + "\n"
        message += "사망".ljust(6) + "{:,}".format(casual["deaths"]).rjust(16) + "{:,}".format(ranked["deaths"]).rjust(14) + "\n"
        message += "킬뎃".ljust(6) + "{0:.2f}".format(casual["kd"]).rjust(16) + "{0:.2f}".format(ranked["kd"]).rjust(14) + "\n"
        message += "승리".ljust(6) + "{:,}".format(casual["wins"]).rjust(16) + "{:,}".format(ranked["wins"]).rjust(14) + "\n"
        message += "패배".ljust(6) + "{:,}".format(casual["losses"]).rjust(16) + "{:,}".format(ranked["losses"]).rjust(14) + "\n"
        message += "승/패".ljust(6) + str(casual["wl"]).rjust(16) + str(ranked["wl"]).rjust(14) + "\n"
        #message += "|" + "".center(18, '-') + "|" + "".center(13, '-') + "|" + "".center(13, '-') + "|" + "\n"
        message += '```'
        return message

    except Exception as ex:
        print('At search_stats(): ')
        err = "ERROR: " + str(ex)
        print(ex)
        return err

def search_operator(ubisoft_id):
    try:
        stat_json = _search(ubisoft_id)
        if 'error' in stat_json:
            if not stat_json['error'].startswith('ERROR:'):
                return 'ERROR: ' + stat_json['error'], None

            return stat_json['error'], None

        operator_list = stat_json['operators']
        message = ''
        message += "**플레이어** : {}\n\n".format(stat_json['username'])

        # 플탐기준 상위 5명만 보여준다
        operator_list = sorted(operator_list, key=lambda operator: operator['playtime'], reverse=True)
        for i in range(0, 5):
            message += "**" + operator_list[i]['operator']['name'].ljust(10) + "**"

            message += '```'
            message += "사살".rjust(2)
            message += "사망".rjust(4)
            message += "킬뎃".rjust(4)
            #message += "승리".rjust(4)
            #message += "패배".rjust(4)
            message += "승률".rjust(4)
            #message += "헤드샷율".rjust(6)

            # timestamp 관련 에러로 임시 주석처리
            # message += "플탐".rjust(7)
            message += "\n".rjust(5)
            message += "{:,}".format(operator_list[i]['kills']).rjust(3)
            message += "{:,}".format(operator_list[i]['deaths']).rjust(6)
            message += "{0:.2f}".format(operator_list[i]['kd']).rjust(6)
            #message += "{:,}".format(operator_list[i]['wins']).rjust(5)
            #message += "{:,}".format(operator_list[i]['losses']).rjust(6)
            message += "{0:.2f}".format(operator_list[i]['wl']).rjust(6)
            # message += "{:,}".format(operator_list[i]['headshots']).rjust(5)
            # message += "{0:.2f}".format(operator_list[i]['headshots'] * 100 / operator_list[i]['kills']).rjust(9)

            # timestamp 관련 에러로 임시 주석처리
            # message += str(datetime.datetime.fromtimestamp(operator_list[i]['playtime']).strftime('%dd %Hh %Mm')).rjust(12)
            message += '\n'
            for abilities in operator_list[i]['abilities']:
                message += (abilities['title'] + ": " + "{:,}".format(abilities['value']) + "\n")
            message += "\n"
            message += '```\n'

        return message, operator_list[0]['operator']['images']['bust']

    except Exception as ex:
        print('At search_operator(): ')
        err = "ERROR: " + str(ex)
        print(ex)
        return err, None


def _search_ubisoft_id(id):
    try:
        # [190226][HKPARK] r6stats api 를 새로 찾아서 그 기능 활용
        res = requests.get('https://r6stats.com/api/player-search/' + id + '/pc', headers={'User-Agent': 'Mozilla/5.0'}, timeout=20)
        json_object_list = json.loads(res.text)
        if res.status_code == 404:
            return 'ERROR: no_record_found'
        elif res.status_code != 200:
            print(res.status_code)
            return 'ERROR: internal_server_error'

        # [190308][HKPARK] 먼저 정확하게 일치하는 것이 있는지 확인 후 리턴
        for json_object in json_object_list:
            if json_object['username'].lower() == id.lower():
                return json_object['ubisoft_id']

        return json_object_list[0]['ubisoft_id']

    except (requests.exceptions.ConnectionError, TimeoutError, requests.exceptions.Timeout,
                requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout) as ex:
        print('At _search_ubisoft_id(): ')
        print(ex)
        return 'ERROR: timeout'

    except Exception as ex:
        print('At _search_ubisoft_id(): ')
        err = 'ERROR: ' + str(ex)
        print(err)
        return err


def _search(ubisoft_id):
    try:
        res = requests.get('https://r6stats.com/api/stats/' + ubisoft_id, headers={'User-Agent': 'Mozilla/5.0'}, timeout=30)
        return json.loads(res.text)

    except (requests.exceptions.ConnectionError, TimeoutError, requests.exceptions.Timeout,
                requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout) as ex:
        print('At _search(): ')
        print(ex)
        err_json = {}
        err_json['error'] = 'ERROR: timeout'
        return err_json

    except Exception as ex:
        print('At _search(): ')
        err_json = {}
        err = 'ERROR: ' + str(ex)
        print(err)
        err_json['error'] = err
        return err_json
