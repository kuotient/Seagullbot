import urllib.request
from bs4 import BeautifulSoup
import json
import r6sapi as api
import requests
import prettytable

def search(id):
    res = requests.get('https://r6stats.com/search/' + id + '/pc/', headers={'User-Agent': 'Mozilla/5.0'})
    bs = BeautifulSoup(res.text, 'html.parser')
    link = bs.select('#__layout > div > div.search-results__wrapper > div > div > div.card > div > div > div > a')
    if len(link) == 0:
        return None
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

    operator = {
        'favorite': bs.select('''#__layout > div > div.player-stats > div.player-header__wrapper > 
                            div > div > div.player-header__left-side > img''')[0].get('alt')
    }

    table_2r = prettytable.PrettyTable(['', '총괄'])
    table_2r.add_row(['플레이한 타임', overall["playtime"]])
    table_2r.add_row(['플레이한 매치', overall["playmatch"]])
    table_2r.add_row(['매치당 사살', overall["k/m"]])
    table_2r.add_row(['사살', overall["kills"]])
    table_2r.add_row(['사망', overall["deaths"]])
    table_2r.add_row(['킬뎃', overall["kd"]])
    table_2r.add_row(['승리', overall["wins"]])
    table_2r.add_row(['패배', overall["losses"]])
    table_2r.add_row(['승/패', overall["wlr"]])
    table_2r.add_row(['눈먼 사살', overall["blind_kills"]])
    table_2r.add_row(['근접 사살', overall["melee_kills"]])
    table_2r.add_row(['관통 사살', overall["penet_kills"]])
    table_2r.add_row(['헤드샷', overall["headshot"]])
    table_2r.add_row(['헤드샷 비율', overall["head_ratio"]])
    table_2r.add_row(['선호 오퍼', overall["fav_oper"]])

    table_3r = prettytable.PrettyTable(['', '캐주얼', '랭크'])
    table_3r.add_row(['플레이한 타임', casual["playtime"], ranked["playtime"]])
    table_3r.add_row(['플레이한 매치', casual["playmatch"], ranked["playmatch"]])
    table_3r.add_row(['매치당 사살', casual["k/m"], ranked["k/m"]])
    table_3r.add_row(['사살', casual["kills"], ranked["kills"]])
    table_3r.add_row(['사망', casual["deaths"], ranked["deaths"]])
    table_3r.add_row(['킬뎃', casual["kd"], ranked["kd"]])
    table_3r.add_row(['승리', casual["wins"], ranked["wins"]])
    table_3r.add_row(['패배', casual["losses"], ranked["losses"]])
    table_3r.add_row(['승/패', casual["wlr"], ranked["wlr"]])

    return '```플레이어 : ' + id + '\n' + table_2r.get_string() + '\n' + table_3r.get_string() + '```'

    # message = ''
    # message += "플레이어 : {}\n\n".format(id)
    # message += "전체\t|\t캐주얼\t\t|\t랭크\n"
    # message += "사살\t|\t{}\t\t|\t{}\n".format(casual["kills"], ranked["kills"])
    # message += "사망\t|\t{}\t\t|\t{}\n".format(casual["deaths"], ranked["deaths"])
    # message += "킬뎃\t|\t{}\t\t|\t{}\n".format(casual["kd"], ranked["kd"])
    # message += "승리\t|\t{}\t\t|\t{}\n".format(casual["wins"], ranked["wins"])
    # message += "패배\t|\t{}\t\t|\t{}\n".format(casual["losses"], ranked["losses"])
    # message += "승/패\t|\t{}\t\t|\t{}\n".format(casual["wlr"], ranked["wlr"])
    # return message

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

