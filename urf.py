import urllib.request
from bs4 import BeautifulSoup


req = urllib.request.Request("http://www.op.gg/urf/statistics")
data = urllib.request.urlopen(req).read()

bs = BeautifulSoup(data, 'html.parser')

l = bs.find_all('td')
l2 = bs.find_all('div')


def urf_rank():
    winrate = []
    champions = []
    kda = []

    for s in l:
        try:
            prop = s.get('class')
            if prop[1] == 'champion-index-table__cell--value':
                str = s.get_text()
                if '%' in str:
                    winrate.append(str)
                elif ':' in str:
                    kda.append(str)

        except UnicodeEncodeError:
            print("Errror")


    for s in l2:
        try:
            prop = s.get('class')
            if prop != None and prop[0] == "champion-index-table__name":
                champions.append(s.get_text())

        except UnicodeEncodeError:
            print("Errror")
    """
    print (champions)
    print(winrate)
    print(kda)
    """
    return (champions,winrate,kda)