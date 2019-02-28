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

    #utils.execute_after(client.send_typing, parameters=message.channel, delay=9)
    await client.send_typing(message.channel)
    ubisoft_id = _search_ubisoft_id(player_id)
    if ubisoft_id is None:
        result = '플레이어를 찾을 수 없습니다.'
        await client.send_message(message.channel, result)
        await client.delete_message(searching)
        return

    result = search_stats(ubisoft_id)
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

    await client.send_typing(message.channel)

    ubisoft_id = _search_ubisoft_id(player_id)
    if ubisoft_id is None:
        result = '플레이어를 찾을 수 없습니다.'
        await client.send_message(message.channel, result)
        await client.delete_message(searching)
        return

    result = search_operator(ubisoft_id)
    embed = discord.Embed(title='***:bomb: RAINBOW SIX STATS :bomb:** presented by* r6stats',
                          description=result + "\n**보다 자세한 정보는 [r6stats](https://r6stats.com/stats/" + ubisoft_id + "/operators)**",
                          color=0x879396)
    embed.set_thumbnail(url="https://ubisoft-avatars.akamaized.net/" + ubisoft_id + "/default_256_256.png")
    # embed.set_footer(text=)
    await client.send_message(message.channel, embed=embed)
    await client.delete_message(searching)
    # await client.delete_message(searching)
    # for result in result_list:
    #     await client.send_message(message.channel, result)


def search_stats(ubisoft_id):
    try:
        stat_json = _search(ubisoft_id)

        if stat_json is None:
            return '처리 중 오류가 발생하였습니다.'
        elif 'error' in stat_json:
            if stat_json['error'] == 'no_records_found':
                return '플레이어가 존재하지 않습니다.'
            else:
                return '처리 중 오류가 발생하였습니다.'

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

        #
        # res = requests.get('https://r6stats.com/search/' + id + '/pc/', headers={'User-Agent': 'Mozilla/5.0'})
        # bs = BeautifulSoup(res.text, 'html.parser')
        # link = bs.select('#__layout > div > div.search-results__wrapper > div > div > div.card > div > div > div > a')
        # if len(link) == 0:
        #     return '플레이어를 찾을수 없습니다.'
        # href = link[0].get('href')
        # res = requests.get('https://r6stats.com' + href, headers={'User-Agent': 'Mozilla/5.0'})
        # bs = BeautifulSoup(res.text, 'html.parser')
        #
        # overall = {
        #     'playtime': bs.select('''#__layout > div > div.player-stats > div.stats-display__wrapper >
        #                             div > div > div > div.player-stats__stats > div.stats-center >
        #                             div.card.stat-card.block__overall.horizontal > div.card__content >
        #                             div.stat-section.wide > span''')[0].get_text(),
        #     'playmatch': bs.select('''#__layout > div > div.player-stats > div.stats-display__wrapper >
        #                             div > div > div > div.player-stats__stats > div.stats-center >
        #                             div.card.stat-card.block__overall.horizontal > div.card__content >
        #                             div:nth-of-type(2) > span''')[0].get_text(),
        #     'k/m': bs.select('''#__layout > div > div.player-stats > div.stats-display__wrapper >
        #                                 div > div > div > div.player-stats__stats > div.stats-center >
        #                                 div.card.stat-card.block__overall.horizontal > div.card__content >
        #                                 div:nth-of-type(3) > span''')[0].get_text(),
        #     'kills': bs.select('''#__layout > div > div.player-stats > div.stats-display__wrapper >
        #                             div > div > div > div.player-stats__stats > div.stats-center >
        #                             div.card.stat-card.block__overall.horizontal > div.card__content >
        #                             div:nth-of-type(4) > span''')[0].get_text(),
        #     'deaths': bs.select('''#__layout > div > div.player-stats > div.stats-display__wrapper >
        #                             div > div > div > div.player-stats__stats > div.stats-center >
        #                             div.card.stat-card.block__overall.horizontal > div.card__content >
        #                             div:nth-of-type(5) > span''')[0].get_text(),
        #     'kd': bs.select('''#__layout > div > div.player-stats > div.stats-display__wrapper >
        #                             div > div > div > div.player-stats__stats > div.stats-center >
        #                             div.card.stat-card.block__overall.horizontal > div.card__content >
        #                             div:nth-of-type(6) > span''')[0].get_text(),
        #     'wins': bs.select('''#__layout > div > div.player-stats > div.stats-display__wrapper >
        #                             div > div > div > div.player-stats__stats > div.stats-center >
        #                             div.card.stat-card.block__overall.horizontal > div.card__content >
        #                             div:nth-of-type(7) > span''')[0].get_text(),
        #     'losses': bs.select('''#__layout > div > div.player-stats > div.stats-display__wrapper >
        #                             div > div > div > div.player-stats__stats > div.stats-center >
        #                             div.card.stat-card.block__overall.horizontal > div.card__content >
        #                             div:nth-of-type(8) > span''')[0].get_text(),
        #     'wlr': bs.select('''#__layout > div > div.player-stats > div.stats-display__wrapper >
        #                             div > div > div > div.player-stats__stats > div.stats-center >
        #                             div.card.stat-card.block__overall.horizontal > div.card__content >
        #                             div:nth-of-type(9) > span''')[0].get_text(),
        #     'blind_kills': bs.select('''#__layout > div > div.player-stats > div.stats-display__wrapper >
        #                             div > div > div > div.player-stats__stats > div.stats-center >
        #                             div.card-wrapper.block__kills > div > div.card__content >
        #                             div:nth-of-type(2) > span''')[0].get_text(),
        #     'melee_kills': bs.select('''#__layout > div > div.player-stats > div.stats-display__wrapper >
        #                             div > div > div > div.player-stats__stats > div.stats-center >
        #                             div.card-wrapper.block__kills > div > div.card__content >
        #                             div:nth-of-type(3) > span''')[0].get_text(),
        #     'penet_kills': bs.select('''#__layout > div > div.player-stats > div.stats-display__wrapper >
        #                             div > div > div > div.player-stats__stats > div.stats-center >
        #                             div.card-wrapper.block__kills > div > div.card__content >
        #                             div:nth-of-type(4) > span''')[0].get_text(),
        #     'headshot': bs.select('''#__layout > div > div.player-stats > div.stats-display__wrapper >
        #                             div > div > div > div.player-stats__stats > div.stats-center >
        #                             div.card-wrapper.block__kills > div > div.card__content >
        #                             div:nth-of-type(5) > span''')[0].get_text(),
        #     'head_ratio': bs.select('''#__layout > div > div.player-stats > div.stats-display__wrapper >
        #                             div > div > div > div.player-stats__stats > div.stats-center >
        #                             div.card-wrapper.block__kills > div > div.card__content >
        #                             div:nth-of-type(6) > span''')[0].get_text(),
        #     'fav_oper': bs.select('''#__layout > div > div.player-stats > div.player-header__wrapper >
        #                         div > div > div.player-header__left-side > img''')[0].get('alt')
        # }
        #
        # casual = {
        #     'playtime': bs.select('''#__layout > div > div.player-stats > div.stats-display__wrapper >
        #                             div > div > div > div.player-stats__stats > div.stats-center >
        #                             div.card.stat-card.block__casual.horizontal > div.card__content >
        #                             div.stat-section.wide > span''')[0].get_text(),
        #     'playmatch': bs.select('''#__layout > div > div.player-stats > div.stats-display__wrapper >
        #                             div > div > div > div.player-stats__stats > div.stats-center >
        #                             div.card.stat-card.block__casual.horizontal > div.card__content >
        #                             div:nth-of-type(2) > span''')[0].get_text(),
        #     'k/m': bs.select('''#__layout > div > div.player-stats > div.stats-display__wrapper >
        #                             div > div > div > div.player-stats__stats > div.stats-center >
        #                             div.card.stat-card.block__casual.horizontal > div.card__content >
        #                             div:nth-of-type(3) > span''')[0].get_text(),
        #     'kills': bs.select('''#__layout > div > div.player-stats > div.stats-display__wrapper >
        #                         div > div > div > div.player-stats__stats > div.stats-center >
        #                         div.card.stat-card.block__casual.horizontal > div.card__content >
        #                         div:nth-of-type(4) > span''')[0].get_text(),
        #     'deaths': bs.select('''#__layout > div > div.player-stats > div.stats-display__wrapper >
        #                         div > div > div > div.player-stats__stats > div.stats-center >
        #                         div.card.stat-card.block__casual.horizontal > div.card__content >
        #                         div:nth-of-type(5) > span''')[0].get_text(),
        #     'kd': bs.select('''#__layout > div > div.player-stats > div.stats-display__wrapper >
        #                         div > div > div > div.player-stats__stats > div.stats-center >
        #                         div.card.stat-card.block__casual.horizontal > div.card__content >
        #                         div:nth-of-type(6) > span''')[0].get_text(),
        #     'wins': bs.select('''#__layout > div > div.player-stats > div.stats-display__wrapper >
        #                         div > div > div > div.player-stats__stats > div.stats-center >
        #                         div.card.stat-card.block__casual.horizontal > div.card__content >
        #                         div:nth-of-type(7) > span''')[0].get_text(),
        #     'losses': bs.select('''#__layout > div > div.player-stats > div.stats-display__wrapper >
        #                         div > div > div > div.player-stats__stats > div.stats-center >
        #                         div.card.stat-card.block__casual.horizontal > div.card__content >
        #                         div:nth-of-type(8) > span''')[0].get_text(),
        #     'wlr': bs.select('''#__layout > div > div.player-stats > div.stats-display__wrapper >
        #                         div > div > div > div.player-stats__stats > div.stats-center >
        #                         div.card.stat-card.block__casual.horizontal > div.card__content >
        #                         div:nth-of-type(9) > span''')[0].get_text()
        # }
        #
        # ranked = {
        #     'playtime': bs.select('''#__layout > div > div.player-stats > div.stats-display__wrapper >
        #                     div > div > div > div.player-stats__stats > div.stats-center >
        #                     div.card.stat-card.block__ranked.horizontal > div.card__content >
        #                     div.stat-section.wide > span''')[0].get_text(),
        #     'playmatch': bs.select('''#__layout > div > div.player-stats > div.stats-display__wrapper >
        #                     div > div > div > div.player-stats__stats > div.stats-center >
        #                     div.card.stat-card.block__ranked.horizontal > div.card__content >
        #                     div:nth-of-type(2) > span''')[0].get_text(),
        #     'k/m': bs.select('''#__layout > div > div.player-stats > div.stats-display__wrapper >
        #                     div > div > div > div.player-stats__stats > div.stats-center >
        #                     div.card.stat-card.block__ranked.horizontal > div.card__content >
        #                     div:nth-of-type(3) > span''')[0].get_text(),
        #     'kills': bs.select('''#__layout > div > div.player-stats > div.stats-display__wrapper >
        #                 div > div > div > div.player-stats__stats > div.stats-center >
        #                 div.card.stat-card.block__ranked.horizontal > div.card__content >
        #                 div:nth-of-type(4) > span''')[0].get_text(),
        #     'deaths': bs.select('''#__layout > div > div.player-stats > div.stats-display__wrapper >
        #                 div > div > div > div.player-stats__stats > div.stats-center >
        #                 div.card.stat-card.block__ranked.horizontal > div.card__content >
        #                 div:nth-of-type(5) > span''')[0].get_text(),
        #     'kd': bs.select('''#__layout > div > div.player-stats > div.stats-display__wrapper >
        #                 div > div > div > div.player-stats__stats > div.stats-center >
        #                 div.card.stat-card.block__ranked.horizontal > div.card__content >
        #                 div:nth-of-type(6) > span''')[0].get_text(),
        #     'wins': bs.select('''#__layout > div > div.player-stats > div.stats-display__wrapper >
        #                 div > div > div > div.player-stats__stats > div.stats-center >
        #                 div.card.stat-card.block__ranked.horizontal > div.card__content >
        #                 div:nth-of-type(7) > span''')[0].get_text(),
        #     'losses': bs.select('''#__layout > div > div.player-stats > div.stats-display__wrapper >
        #                 div > div > div > div.player-stats__stats > div.stats-center >
        #                 div.card.stat-card.block__ranked.horizontal > div.card__content >
        #                 div:nth-of-type(8) > span''')[0].get_text(),
        #     'wlr': bs.select('''#__layout > div > div.player-stats > div.stats-display__wrapper >
        #                 div > div > div > div.player-stats__stats > div.stats-center >
        #                 div.card.stat-card.block__ranked.horizontal > div.card__content >
        #                 div:nth-of-type(9) > span''')[0].get_text(),
        # }


        # message = '```'
        # message += "플레이어 : {}\n\n".format(id)
        #
        # message += "".rjust(20) + "총괄".rjust(13) + "\n\n"
        # message += "플레이한 시간".rjust(15) + overall["playtime"].rjust(13) + "\n"
        # message += "플레이한 매치".rjust(15) + overall["playmatch"].rjust(13) + "\n"
        # message += "매치당 사살 수".rjust(15) + overall["k/m"].rjust(13) + "\n"
        # message += "사살".rjust(18) + overall["kills"].rjust(13) + "\n"
        # message += "사망".rjust(18) + overall["deaths"].rjust(13) + "\n"
        # message += "킬뎃".rjust(18) + overall["kd"].rjust(13) + "\n"
        # message += "승리".rjust(18) + overall["wins"].rjust(13) + "\n"
        # message += "패배".rjust(18) + overall["losses"].rjust(13) + "\n"
        # message += "승/패".rjust(18) + overall["wlr"].rjust(13) + "\n"
        # message += "눈먼 사살".rjust(16) + overall["blind_kills"].rjust(13) + "\n"
        # message += "근접 사살".rjust(16) + overall["melee_kills"].rjust(13) + "\n"
        # message += "관통 사살".rjust(16) + overall["penet_kills"].rjust(13) + "\n"
        # message += "헤드샷".rjust(17) + overall["headshot"].rjust(13) + "\n"
        # message += "헤드샷 비율".rjust(15) + overall["head_ratio"].rjust(13) + "\n"
        # message += "선호 오퍼".rjust(16) + overall["fav_oper"].rjust(13) + "\n\n"
        # message += "".rjust(47, '-') + '\n\n'
        # message += "".rjust(20) + "캐주얼".rjust(13) + "랭크".rjust(13) + "\n\n"
        # #message += "|" + "".center(18, '-') + "|" + "".center(13, '-') + "|" + "".center(13, '-') + "|" + "\n"
        # message += "사살".rjust(18) + casual["kills"].rjust(16) + ranked["kills"].rjust(13) + "\n"
        # message += "사망".rjust(18) + casual["deaths"].rjust(16) + ranked["deaths"].rjust(13) + "\n"
        # message += "킬뎃".rjust(18) + casual["kd"].rjust(16) + ranked["kd"].rjust(13) + "\n"
        # message += "승리".rjust(18) + casual["wins"].rjust(16) + ranked["wins"].rjust(13) + "\n"
        # message += "패배".rjust(18) + casual["losses"].rjust(16) + ranked["losses"].rjust(13) + "\n"
        # message += "승/패".rjust(18) + casual["wlr"].rjust(16) + ranked["wlr"].rjust(13) + "\n"
        # #message += "|" + "".center(18, '-') + "|" + "".center(13, '-') + "|" + "".center(13, '-') + "|" + "\n"
        # message += '```'
        # return message


    except Exception as ex:
        print(ex)
        return '처리 중 오류가 발생하였습니다.'

def search_operator(ubisoft_id):
    try:
        stat_json = _search(ubisoft_id)

        if stat_json is None:
            return '처리 중 오류가 발생하였습니다.'
        elif 'error' in stat_json:
            if stat_json['error'] == 'no_records_found':
                return '플레이어가 존재하지 않습니다.'
            else:
                return '처리 중 오류가 발생하였습니다.'

        operator_list = stat_json['operators']

        message = ''

        message += "**플레이어** : {}\n\n".format(stat_json['username'])

        # message += "오퍼".center(5)


        # 플탐기준 상위 5명만 보여준다
        operator_list = sorted(operator_list, key=lambda operator: operator['playtime'], reverse=True)
        for i in range(0, 5):
            message += "**" + operator_list[i]['operator']['name'].ljust(10) + "**"

            message += '```'
            message += "사살".rjust(3)
            message += "사망".rjust(4)
            message += "킬뎃".rjust(4)
            #message += "승리".rjust(4)
            #message += "패배".rjust(4)
            message += "승률".rjust(4)
            #message += "헤드샷율".rjust(6)
            message += "플탐".rjust(7)
            message += "\n".rjust(7)
            message += "{:,}".format(operator_list[i]['kills']).rjust(4)
            message += "{:,}".format(operator_list[i]['deaths']).rjust(6)
            message += "{0:.2f}".format(operator_list[i]['kd']).rjust(6)
            #message += "{:,}".format(operator_list[i]['wins']).rjust(5)
            #message += "{:,}".format(operator_list[i]['losses']).rjust(6)
            message += "{0:.2f}".format(operator_list[i]['wl']).rjust(6)
            # message += "{:,}".format(operator_list[i]['headshots']).rjust(5)
            # message += "{0:.2f}".format(operator_list[i]['headshots'] * 100 / operator_list[i]['kills']).rjust(9)
            message += str(datetime.datetime.fromtimestamp(operator_list[i]['playtime']).strftime('%dd %Hh %Mm')).rjust(13) + "\n"
            for abilities in operator_list[i]['abilities']:
                message += (abilities['title'] + ": " + "{:,}".format(abilities['value']) + "\n")
            message += "\n"
            message += '```\n'

        return message

    except Exception as ex:
        print(ex)
        return '처리 중 오류가 발생하였습니다.'

    #
    #     res = requests.get('https://r6stats.com/search/' + id + '/pc/', headers={'User-Agent': 'Mozilla/5.0'})
    #     bs = BeautifulSoup(res.text, 'html.parser')
    #     link = bs.select('#__layout > div > div.search-results__wrapper > div > div > div.card > div > div > div > a')
    #     if len(link) == 0:
    #         return '플레이어를 찾을수 없습니다.'
    #     href = link[0].get('href')
    #     options = webdriver.ChromeOptions()
    #     options.add_argument('headless')
    #     options.add_argument('window-size=1920x1080')
    #     options.add_argument("disable-gpu")
    #     driver = webdriver.Chrome(CHROME_PATH, chrome_options=options)
    #
    #     #res = requests.get('https://r6stats.com' + href + 'operators', headers={'User-Agent': 'Mozilla/5.0'})
    #     # bs = BeautifulSoup(res.text, 'html.parser')
    #     driver.get('https://r6stats.com' + href + 'operators')
    #     row_list = driver.find_elements_by_css_selector(
    #         '''#__layout > div > div.player-stats > div.stats-display__wrapper >
    #         div > div > div > div.card > div > div.table__responsive-overflow-wrapper >
    #         table > tbody > tr'''
    #     )
    #
    #     for row in row_list:
    #         row.click()
    #
    #     bs = BeautifulSoup(driver.page_source, 'html.parser')
    #
    #     operator_data = bs.select('''#__layout > div > div.player-stats > div.stats-display__wrapper >
    #                     div > div > div > div.card > div > div.table__responsive-overflow-wrapper >
    #                      table > tbody > tr''')
    #
    #     operator_dic = {}
    #     operator_name_list = []
    #     operator_special_dic = {}
    #     temp = bs.select('''#__layout > div > div.player-stats > div.stats-display__wrapper > div >
    #                     div > div > div.card > div > div.table__responsive-overflow-wrapper > table >
    #                     tbody > tr:nth-of-type(1) > td.operator__info > span''')[0].get_text()
    #     for operator_data_row in operator_data:
    #         if 'secondary-row' in operator_data_row['class']:
    #             operator_special_list = []
    #             for operator_special_td in operator_data_row.select('td div.operator__special'):
    #                 operator_special_title = operator_special_td.select('div.operator__special__title')[0].get_text()
    #                 operator_special_value = operator_special_td.select('div.operator__special__value')[0].get_text()
    #                 operator_special_list.append([operator_special_title, operator_special_value])
    #             operator_special_dic[temp] = operator_special_list
    #         else:
    #             operator_data_list = []
    #             for operator_data_row_td in operator_data_row.select('td'):
    #                 operator_data_list.append(operator_data_row_td.get_text())
    #             operator_dic[operator_data_row.select('td.operator__info > span')[0].get_text()] = operator_data_list
    #             temp = operator_data_row.select('td.operator__info > span')[0].get_text()
    #
    #
    #
    #     # __layout > div > div.player-stats > div.stats-display__wrapper > div > div > div > div.card > div > div.table__responsive-overflow-wrapper > table > tbody > tr.operator__special__row.secondary-row
    #     #body > script:nth-child(2)
    #     ret_list = []
    #     counter = 0
    #     message = '```'
    #     message += "플레이어 : {}\n\n".format(id)
    #     message += "오퍼레이터".rjust(8)
    #     message += "사살".rjust(5)
    #     message += "사망".rjust(3)
    #     message += "킬뎃".rjust(2)
    #     message += "승리".rjust(6)
    #     message += "패배".rjust(6)
    #     message += "승/패".rjust(6)
    #     message += "헤드샷".rjust(6)
    #     message += "근접공격".rjust(6)
    #     message += "기절시킨 수".rjust(6)
    #     message += "플레이한 시간".rjust(6)
    #     message += "\n\n"
    #
    #     for operator in list(operator_dic.keys()):
    #         message += operator.rjust(11)
    #         for i in range(1, 11):
    #             message += operator_dic[operator][i].rjust(6)
    #         message += '\n'
    #         for i in range(0, len(operator_special_dic[operator])):
    #             message += ', ' if i is not 0 else ''
    #             message += operator_special_dic[operator][i][0]
    #             message += operator_special_dic[operator][i][1]
    #
    #         message += '\n'
    #         counter += 1
    #         if counter <= 5:
    #             continue
    #
    #         message += '```'
    #         ret_list.append(message)
    #         message = '```'
    #         counter = 0
    #
    #     message += '```'
    #     ret_list.append(message)
    #     return ret_list
    #
    # except Exception as ex:
    #     print(ex)
    #     return '처리 중 오류가 발생하였습니다.'


def _search_ubisoft_id(id):
    try:
        # [190226][HKPARK] r6stats api 를 새로 찾아서 그 기능 활용
        res = requests.get('https://r6stats.com/api/player-search/' + id + '/pc', headers={'User-Agent': 'Mozilla/5.0'})
        jsonObject = json.loads(res.text)
        if res.status_code != 200:
            return None

        return jsonObject[0]['ubisoft_id']

    except Exception as ex:
        print(ex)
        return None

def _search(ubisoft_id):
    try:
        res = requests.get('https://r6stats.com/api/stats/' + ubisoft_id, headers={'User-Agent': 'Mozilla/5.0'})
        return json.loads(res.text)

    except Exception as ex:
        print(ex)
        return None