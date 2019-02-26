import urllib.request
from bs4 import BeautifulSoup
import json
import requests
import prettytable

def pubg_search(id):
    res = requests.get('https://pubg.op.gg/user/' + id , headers={'User-Agent': 'Mozilla/5.0'})
    bs = BeautifulSoup(res.text, 'html.parser')
    link = bs.select('#matchDetailWrap > div.user-content-layer__matches-content > div:nth-of-type(1) > div > div > div.user-content-layer__matches-list > ul')
    if len(link) == 0:
        return '플레이어를 찾을 수 없습니다.'
    overall={
        'recent':bs.selct('''#matchDetailWrap > div.user-content-layer__matches-content > div:nth-of-type(1) > div > div > div.user-content-layer__matches-list''')[0].get_text(),
        'rank': bs.select('''#matchDetailWrap > div.user-content-layer__matches-content > div:nth-of-type(1) > div > div > div.user-content-layer__matches-list > ul > li:nth-child(1) > div.matches-item__summary > div.matches-item__column.matches-item__column--kill''')[0].get_text(),
        'kill':bs.select('''#matchDetailWrap > div.user-content-layer__matches-content > div:nth-of-type(1) > div > div > div.user-content-layer__matches-list > ul > li:nth-child(1) > div.matches-item__summary > div.matches-item__column.matches-item__column--kill > div.matches-item__value''')[0].get_text(),
    }
    message = '```'
    message += "플레이어 : {}\n\n".format(id)

    message += "최근 게임".ljust(15) + overall["recent"].ljust(13) + "\n"
    message += "순위".ljust(15) + overall["rank"].ljust(13) + "\n"
    message += "킬수".ljust(15) + overall["kill"].ljust(13) + "\n"
    message += '```'
    return message
