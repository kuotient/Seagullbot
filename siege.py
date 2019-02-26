import urllib.request
from bs4 import BeautifulSoup
import json
import requests
import prettytable
from selenium import webdriver

PHANTOMJS_PATH = 'phantomjs.exe'

CHROME_PATH = 'chromedriver.exe'


async def siege_search(argv, argc, client, message):
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
    result = search(player_id)
    await client.send_message(message.channel, result)
    await client.edit_message(searching, '***:bomb: RAINBOW SIX STATS :bomb:** presented by* r6stats')


async def siege_search_operator(argv, argc, client, message):
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
    result_list = search_operator(player_id)
    await client.delete_message(searching)
    for result in result_list:
        await client.send_message(message.channel, result)


def search(id):
    try:
        res = requests.get('https://r6stats.com/search/' + id + '/pc/', headers={'User-Agent': 'Mozilla/5.0'})
        bs = BeautifulSoup(res.text, 'html.parser')
        link = bs.select('#__layout > div > div.search-results__wrapper > div > div > div.card > div > div > div > a')
        if len(link) == 0:
            return '플레이어를 찾을수 없습니다.'
        href = link[0].get('href')
        res = requests.get('https://r6stats.com' + href, headers={'User-Agent': 'Mozilla/5.0'})
        bs = BeautifulSoup(res.text, 'html.parser')

        overall = {
            'playtime': bs.select('''#__layout > div > div.player-stats > div.stats-display__wrapper > 
                                    div > div > div > div.player-stats__stats > div.stats-center > 
                                    div.card.stat-card.block__overall.horizontal > div.card__content > 
                                    div.stat-section.wide > span''')[0].get_text(),
            'playmatch': bs.select('''#__layout > div > div.player-stats > div.stats-display__wrapper >
                                    div > div > div > div.player-stats__stats > div.stats-center > 
                                    div.card.stat-card.block__overall.horizontal > div.card__content > 
                                    div:nth-of-type(2) > span''')[0].get_text(),
            'k/m': bs.select('''#__layout > div > div.player-stats > div.stats-display__wrapper >
                                        div > div > div > div.player-stats__stats > div.stats-center > 
                                        div.card.stat-card.block__overall.horizontal > div.card__content > 
                                        div:nth-of-type(3) > span''')[0].get_text(),
            'kills': bs.select('''#__layout > div > div.player-stats > div.stats-display__wrapper >
                                    div > div > div > div.player-stats__stats > div.stats-center > 
                                    div.card.stat-card.block__overall.horizontal > div.card__content > 
                                    div:nth-of-type(4) > span''')[0].get_text(),
            'deaths': bs.select('''#__layout > div > div.player-stats > div.stats-display__wrapper >
                                    div > div > div > div.player-stats__stats > div.stats-center > 
                                    div.card.stat-card.block__overall.horizontal > div.card__content > 
                                    div:nth-of-type(5) > span''')[0].get_text(),
            'kd': bs.select('''#__layout > div > div.player-stats > div.stats-display__wrapper >
                                    div > div > div > div.player-stats__stats > div.stats-center > 
                                    div.card.stat-card.block__overall.horizontal > div.card__content > 
                                    div:nth-of-type(6) > span''')[0].get_text(),
            'wins': bs.select('''#__layout > div > div.player-stats > div.stats-display__wrapper >
                                    div > div > div > div.player-stats__stats > div.stats-center > 
                                    div.card.stat-card.block__overall.horizontal > div.card__content > 
                                    div:nth-of-type(7) > span''')[0].get_text(),
            'losses': bs.select('''#__layout > div > div.player-stats > div.stats-display__wrapper >
                                    div > div > div > div.player-stats__stats > div.stats-center > 
                                    div.card.stat-card.block__overall.horizontal > div.card__content > 
                                    div:nth-of-type(8) > span''')[0].get_text(),
            'wlr': bs.select('''#__layout > div > div.player-stats > div.stats-display__wrapper >
                                    div > div > div > div.player-stats__stats > div.stats-center > 
                                    div.card.stat-card.block__overall.horizontal > div.card__content > 
                                    div:nth-of-type(9) > span''')[0].get_text(),
            'blind_kills': bs.select('''#__layout > div > div.player-stats > div.stats-display__wrapper >
                                    div > div > div > div.player-stats__stats > div.stats-center > 
                                    div.card-wrapper.block__kills > div > div.card__content > 
                                    div:nth-of-type(2) > span''')[0].get_text(),
            'melee_kills': bs.select('''#__layout > div > div.player-stats > div.stats-display__wrapper >
                                    div > div > div > div.player-stats__stats > div.stats-center > 
                                    div.card-wrapper.block__kills > div > div.card__content > 
                                    div:nth-of-type(3) > span''')[0].get_text(),
            'penet_kills': bs.select('''#__layout > div > div.player-stats > div.stats-display__wrapper >
                                    div > div > div > div.player-stats__stats > div.stats-center > 
                                    div.card-wrapper.block__kills > div > div.card__content > 
                                    div:nth-of-type(4) > span''')[0].get_text(),
            'headshot': bs.select('''#__layout > div > div.player-stats > div.stats-display__wrapper >
                                    div > div > div > div.player-stats__stats > div.stats-center > 
                                    div.card-wrapper.block__kills > div > div.card__content > 
                                    div:nth-of-type(5) > span''')[0].get_text(),
            'head_ratio': bs.select('''#__layout > div > div.player-stats > div.stats-display__wrapper >
                                    div > div > div > div.player-stats__stats > div.stats-center > 
                                    div.card-wrapper.block__kills > div > div.card__content > 
                                    div:nth-of-type(6) > span''')[0].get_text(),
            'fav_oper': bs.select('''#__layout > div > div.player-stats > div.player-header__wrapper > 
                                div > div > div.player-header__left-side > img''')[0].get('alt')
        }

        casual = {
            'playtime': bs.select('''#__layout > div > div.player-stats > div.stats-display__wrapper >
                                    div > div > div > div.player-stats__stats > div.stats-center > 
                                    div.card.stat-card.block__casual.horizontal > div.card__content > 
                                    div.stat-section.wide > span''')[0].get_text(),
            'playmatch': bs.select('''#__layout > div > div.player-stats > div.stats-display__wrapper >
                                    div > div > div > div.player-stats__stats > div.stats-center > 
                                    div.card.stat-card.block__casual.horizontal > div.card__content > 
                                    div:nth-of-type(2) > span''')[0].get_text(),
            'k/m': bs.select('''#__layout > div > div.player-stats > div.stats-display__wrapper >
                                    div > div > div > div.player-stats__stats > div.stats-center > 
                                    div.card.stat-card.block__casual.horizontal > div.card__content > 
                                    div:nth-of-type(3) > span''')[0].get_text(),
            'kills': bs.select('''#__layout > div > div.player-stats > div.stats-display__wrapper >
                                div > div > div > div.player-stats__stats > div.stats-center > 
                                div.card.stat-card.block__casual.horizontal > div.card__content > 
                                div:nth-of-type(4) > span''')[0].get_text(),
            'deaths': bs.select('''#__layout > div > div.player-stats > div.stats-display__wrapper >
                                div > div > div > div.player-stats__stats > div.stats-center > 
                                div.card.stat-card.block__casual.horizontal > div.card__content > 
                                div:nth-of-type(5) > span''')[0].get_text(),
            'kd': bs.select('''#__layout > div > div.player-stats > div.stats-display__wrapper >
                                div > div > div > div.player-stats__stats > div.stats-center > 
                                div.card.stat-card.block__casual.horizontal > div.card__content > 
                                div:nth-of-type(6) > span''')[0].get_text(),
            'wins': bs.select('''#__layout > div > div.player-stats > div.stats-display__wrapper >
                                div > div > div > div.player-stats__stats > div.stats-center > 
                                div.card.stat-card.block__casual.horizontal > div.card__content > 
                                div:nth-of-type(7) > span''')[0].get_text(),
            'losses': bs.select('''#__layout > div > div.player-stats > div.stats-display__wrapper >
                                div > div > div > div.player-stats__stats > div.stats-center > 
                                div.card.stat-card.block__casual.horizontal > div.card__content > 
                                div:nth-of-type(8) > span''')[0].get_text(),
            'wlr': bs.select('''#__layout > div > div.player-stats > div.stats-display__wrapper >
                                div > div > div > div.player-stats__stats > div.stats-center > 
                                div.card.stat-card.block__casual.horizontal > div.card__content > 
                                div:nth-of-type(9) > span''')[0].get_text()
        }

        ranked = {
            'playtime': bs.select('''#__layout > div > div.player-stats > div.stats-display__wrapper >
                            div > div > div > div.player-stats__stats > div.stats-center > 
                            div.card.stat-card.block__ranked.horizontal > div.card__content > 
                            div.stat-section.wide > span''')[0].get_text(),
            'playmatch': bs.select('''#__layout > div > div.player-stats > div.stats-display__wrapper >
                            div > div > div > div.player-stats__stats > div.stats-center > 
                            div.card.stat-card.block__ranked.horizontal > div.card__content > 
                            div:nth-of-type(2) > span''')[0].get_text(),
            'k/m': bs.select('''#__layout > div > div.player-stats > div.stats-display__wrapper >
                            div > div > div > div.player-stats__stats > div.stats-center > 
                            div.card.stat-card.block__ranked.horizontal > div.card__content > 
                            div:nth-of-type(3) > span''')[0].get_text(),
            'kills': bs.select('''#__layout > div > div.player-stats > div.stats-display__wrapper >
                        div > div > div > div.player-stats__stats > div.stats-center > 
                        div.card.stat-card.block__ranked.horizontal > div.card__content > 
                        div:nth-of-type(4) > span''')[0].get_text(),
            'deaths': bs.select('''#__layout > div > div.player-stats > div.stats-display__wrapper >
                        div > div > div > div.player-stats__stats > div.stats-center > 
                        div.card.stat-card.block__ranked.horizontal > div.card__content > 
                        div:nth-of-type(5) > span''')[0].get_text(),
            'kd': bs.select('''#__layout > div > div.player-stats > div.stats-display__wrapper >
                        div > div > div > div.player-stats__stats > div.stats-center > 
                        div.card.stat-card.block__ranked.horizontal > div.card__content > 
                        div:nth-of-type(6) > span''')[0].get_text(),
            'wins': bs.select('''#__layout > div > div.player-stats > div.stats-display__wrapper >
                        div > div > div > div.player-stats__stats > div.stats-center > 
                        div.card.stat-card.block__ranked.horizontal > div.card__content > 
                        div:nth-of-type(7) > span''')[0].get_text(),
            'losses': bs.select('''#__layout > div > div.player-stats > div.stats-display__wrapper >
                        div > div > div > div.player-stats__stats > div.stats-center > 
                        div.card.stat-card.block__ranked.horizontal > div.card__content > 
                        div:nth-of-type(8) > span''')[0].get_text(),
            'wlr': bs.select('''#__layout > div > div.player-stats > div.stats-display__wrapper >
                        div > div > div > div.player-stats__stats > div.stats-center > 
                        div.card.stat-card.block__ranked.horizontal > div.card__content > 
                        div:nth-of-type(9) > span''')[0].get_text(),
        }


        # table_2r = prettytable.PrettyTable(['', 'Overall'])
        # table_2r.add_row(['Played Time', overall["playtime"]])
        # table_2r.add_row(['Played Match', overall["playmatch"]])
        # table_2r.add_row(['Kills / Match', overall["k/m"]])
        # table_2r.add_row(['Kills', overall["kills"]])
        # table_2r.add_row(['Deaths', overall["deaths"]])
        # table_2r.add_row(['K/D', overall["kd"]])
        # table_2r.add_row(['Wins', overall["wins"]])
        # table_2r.add_row(['Loses', overall["losses"]])
        # table_2r.add_row(['Win / Lose', overall["wlr"]])
        # table_2r.add_row(['Blind Kills', overall["blind_kills"]])
        # table_2r.add_row(['Melee Kills', overall["melee_kills"]])
        # table_2r.add_row(['Penetration Kills', overall["penet_kills"]])
        # table_2r.add_row(['Headshots', overall["headshot"]])
        # table_2r.add_row(['Headshots Ratio', overall["head_ratio"]])
        # table_2r.add_row(['Most Favorite Operator', overall["fav_oper"]])
        #
        # table_3r = prettytable.PrettyTable(['', 'Casual', 'Ranked'])
        # table_3r.add_row(['Played Time', casual["playtime"], ranked["playtime"]])
        # table_3r.add_row(['Played Match', casual["playmatch"], ranked["playmatch"]])
        # table_3r.add_row(['Kills / Match', casual["k/m"], ranked["k/m"]])
        # table_3r.add_row(['Kills', casual["kills"], ranked["kills"]])
        # table_3r.add_row(['Deaths', casual["deaths"], ranked["deaths"]])
        # table_3r.add_row(['K/D', casual["kd"], ranked["kd"]])
        # table_3r.add_row(['Wins', casual["wins"], ranked["wins"]])
        # table_3r.add_row(['Loses', casual["losses"], ranked["losses"]])
        # table_3r.add_row(['Win / Lose', casual["wlr"], ranked["wlr"]])
        # return '```플레이어 : ' + id + '\n' + table_2r.get_string() + '\n' + table_3r.get_string() + '```'


        message = '```'
        message += "플레이어 : {}\n\n".format(id)

        message += "".ljust(20) + "총괄".ljust(13) + "\n\n"
        message += "플레이한 시간".ljust(15) + overall["playtime"].ljust(13) + "\n"
        message += "플레이한 매치".ljust(15) + overall["playmatch"].ljust(13) + "\n"
        message += "매치당 사살 수".ljust(15) + overall["k/m"].ljust(13) + "\n"
        message += "사살".ljust(18) + overall["kills"].ljust(13) + "\n"
        message += "사망".ljust(18) + overall["deaths"].ljust(13) + "\n"
        message += "킬뎃".ljust(18) + overall["kd"].ljust(13) + "\n"
        message += "승리".ljust(18) + overall["wins"].ljust(13) + "\n"
        message += "패배".ljust(18) + overall["losses"].ljust(13) + "\n"
        message += "승/패".ljust(18) + overall["wlr"].ljust(13) + "\n"
        message += "눈먼 사살".ljust(16) + overall["blind_kills"].ljust(13) + "\n"
        message += "근접 사살".ljust(16) + overall["melee_kills"].ljust(13) + "\n"
        message += "관통 사살".ljust(16) + overall["penet_kills"].ljust(13) + "\n"
        message += "헤드샷".ljust(17) + overall["headshot"].ljust(13) + "\n"
        message += "헤드샷 비율".ljust(15) + overall["head_ratio"].ljust(13) + "\n"
        message += "선호 오퍼".ljust(16) + overall["fav_oper"].ljust(13) + "\n\n"
        message += "".ljust(47, '-') + '\n\n'
        message += "".ljust(20) + "캐주얼".ljust(13) + "랭크".ljust(13) + "\n\n"
        #message += "|" + "".center(18, '-') + "|" + "".center(13, '-') + "|" + "".center(13, '-') + "|" + "\n"
        message += "사살".ljust(18) + casual["kills"].ljust(16) + ranked["kills"].ljust(13) + "\n"
        message += "사망".ljust(18) + casual["deaths"].ljust(16) + ranked["deaths"].ljust(13) + "\n"
        message += "킬뎃".ljust(18) + casual["kd"].ljust(16) + ranked["kd"].ljust(13) + "\n"
        message += "승리".ljust(18) + casual["wins"].ljust(16) + ranked["wins"].ljust(13) + "\n"
        message += "패배".ljust(18) + casual["losses"].ljust(16) + ranked["losses"].ljust(13) + "\n"
        message += "승/패".ljust(18) + casual["wlr"].ljust(16) + ranked["wlr"].ljust(13) + "\n"
        #message += "|" + "".center(18, '-') + "|" + "".center(13, '-') + "|" + "".center(13, '-') + "|" + "\n"
        message += '```'
        return message


    except Exception as ex:
        print(ex)
        return '처리 중 오류가 발생하였습니다.'


    # [190222][HKPARK] API 있긴한데 느려터져서 크롤링으로 가져오는게 더 빠름
    # req = urllib.request.Request("https://api.r6stats.com/api/v1/players/" + id + "?platform=uplay", headers={'User-Agent': 'Mozilla/5.0'})
    # res = urllib.request.urlopen(req)
    # if res.status == 404:
    #     return None
    # data = res.read()
    # player = json.loads(data.decode('utf-8'))
    # message = ''
    # stats = player["player"]["stats"]
    # actual = player["player"]["username"]
    # ranked = stats["ranked"]
    # casual = stats["casual"]
    # message += "플레이어 : {}:\n\n".format(actual)
    # message += "전체|캐주얼|랭크\n"
    # message += ":---|:---|:---\n"
    # message += "사살|{}|{}\n".format(casual["kills"], ranked["kills"])
    # message += "사망|{}|{}\n".format(casual["deaths"], ranked["deaths"])
    # message += "킬뎃|{}|{}\n".format(casual["kd"], ranked["kd"])
    # message += "승리|{}|{}\n".format(casual["wins"], ranked["wins"])
    # message += "패배|{}|{}\n".format(casual["losses"], ranked["losses"])
    # message += "승/패|{}|{}\n".format(casual["wlr"], ranked["wlr"])
    # return message

def search_operator(id):
    try:
        res = requests.get('https://r6stats.com/search/' + id + '/pc/', headers={'User-Agent': 'Mozilla/5.0'})
        bs = BeautifulSoup(res.text, 'html.parser')
        link = bs.select('#__layout > div > div.search-results__wrapper > div > div > div.card > div > div > div > a')
        if len(link) == 0:
            return '플레이어를 찾을수 없습니다.'
        href = link[0].get('href')
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1920x1080')
        options.add_argument("disable-gpu")
        driver = webdriver.Chrome(CHROME_PATH, chrome_options=options)

        #res = requests.get('https://r6stats.com' + href + 'operators', headers={'User-Agent': 'Mozilla/5.0'})
        # bs = BeautifulSoup(res.text, 'html.parser')
        driver.get('https://r6stats.com' + href + 'operators')
        row_list = driver.find_elements_by_css_selector(
            '''#__layout > div > div.player-stats > div.stats-display__wrapper > 
            div > div > div > div.card > div > div.table__responsive-overflow-wrapper > 
            table > tbody > tr'''
        )

        for row in row_list:
            row.click()

        bs = BeautifulSoup(driver.page_source, 'html.parser')

        operator_data = bs.select('''#__layout > div > div.player-stats > div.stats-display__wrapper >
                        div > div > div > div.card > div > div.table__responsive-overflow-wrapper >
                         table > tbody > tr''')

        operator_dic = {}
        operator_name_list = []
        operator_special_dic = {}
        temp = bs.select('''#__layout > div > div.player-stats > div.stats-display__wrapper > div > 
                        div > div > div.card > div > div.table__responsive-overflow-wrapper > table > 
                        tbody > tr:nth-of-type(1) > td.operator__info > span''')[0].get_text()
        for operator_data_row in operator_data:
            if 'secondary-row' in operator_data_row['class']:
                operator_special_list = []
                for operator_special_td in operator_data_row.select('td div.operator__special'):
                    operator_special_title = operator_special_td.select('div.operator__special__title')[0].get_text()
                    operator_special_value = operator_special_td.select('div.operator__special__value')[0].get_text()
                    operator_special_list.append([operator_special_title, operator_special_value])
                operator_special_dic[temp] = operator_special_list
            else:
                operator_data_list = []
                for operator_data_row_td in operator_data_row.select('td'):
                    operator_data_list.append(operator_data_row_td.get_text())
                operator_dic[operator_data_row.select('td.operator__info > span')[0].get_text()] = operator_data_list
                temp = operator_data_row.select('td.operator__info > span')[0].get_text()



        # __layout > div > div.player-stats > div.stats-display__wrapper > div > div > div > div.card > div > div.table__responsive-overflow-wrapper > table > tbody > tr.operator__special__row.secondary-row
        #body > script:nth-child(2)
        ret_list = []
        counter = 0
        message = '```'
        message += "플레이어 : {}\n\n".format(id)
        message += "오퍼레이터".ljust(8)
        message += "사살".ljust(5)
        message += "사망".ljust(3)
        message += "킬뎃".ljust(2)
        message += "승리".ljust(6)
        message += "패배".ljust(6)
        message += "승/패".ljust(6)
        message += "헤드샷".ljust(6)
        message += "근접공격".ljust(6)
        message += "기절시킨 수".ljust(6)
        message += "플레이한 시간".ljust(6)
        message += "\n\n"

        for operator in list(operator_dic.keys()):
            message += operator.ljust(11)
            for i in range(1, 11):
                message += operator_dic[operator][i].ljust(6)
            message += '\n'
            for i in range(0, len(operator_special_dic[operator])):
                message += ', ' if i is not 0 else ''
                message += operator_special_dic[operator][i][0]
                message += operator_special_dic[operator][i][1]

            message += '\n'
            counter += 1
            if counter <= 5:
                continue

            message += '```'
            ret_list.append(message)
            message = '```'
            counter = 0

        message += '```'
        ret_list.append(message)
        return ret_list

    except Exception as ex:
        print(ex)
        return '처리 중 오류가 발생하였습니다.'

