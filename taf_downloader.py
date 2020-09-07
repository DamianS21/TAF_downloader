import requests

from bs4 import BeautifulSoup
from datetime import datetime

from requests.exceptions import Timeout
import pickle
import re

regex = r"^[0-9]{2}(0[1-9]|1[0-2])(0[1-9]|[1-2][0-9]|3[0-1])([0-9]|0[0-9]|1[0-9]|2[0-3])([0-5][0-9])$"


DEFAULT_PROXIES_LIST = [{'http://13.251.27.133:3128': 1599290728.996448},
 {'http://81.201.60.130:80': 1599290747.885732},
 {'http://83.97.23.90:18080': 1599290753.470598},
 {'http://95.174.67.50:18080': 1599290776.979552},
 {'http://58.120.171.37:8080': 1599290837.672835},
 {'http://103.87.169.240:44139': 1599290877.187446},
 {'http://34.80.14.167:3128': 1599290920.276014},
 {'http://142.44.221.126:8080': 1599291193.038196},
 {'http://13.75.77.214:44355': 1599291205.85588},
 {'http://121.100.24.11:8080': 1599291306.537596},
 {'http://161.202.226.194:80': 1599291422.955892},
 {'http://34.105.59.26:80': 1599291518.469186},
 {'http://14.139.156.110:9797': 1599291649.498366},
 {'http://139.99.105.5:80': 1599291771.663148},
 {'http://191.232.170.36:80': 1599292022.276875},
 {'http://184.23.191.105:8118': 1599292677.842664},
 {'http://103.76.253.154:3128': 1599292947.214033},
 {'http://170.158.99.160:8080': 1599292952.508051},
 {'http://170.185.220.14:8088': 1599292964.629952},
 {'http://170.185.195.14:8088': 1599292967.180643}]

airport_text = input('List of airports ICAO codes separated by a space: ')
airports = airport_text.upper().split()

global proxies_list

try:
    proxies_file = open('proxies.txt', 'rb')
    proxies_list = pickle.load(proxies_file)
    proxies_file.close()
except FileNotFoundError:
    proxies_file = open('proxies.txt','wb')
    pickle.dump(DEFAULT_PROXIES_LIST, proxies_file)
    proxies_file.close()
    proxies_file = open('proxies.txt', 'rb')
    proxies_list = pickle.load(proxies_file)
    proxies_file.close()

while True:
    inp = input('FROM date (format YYMMDDHHMM): ')
    if re.match(regex,inp):
        date_from = inp
        break

while True:
    inp = input('TO date (format YYMMDDHHMM): ')
    if re.match(regex,inp):
        date_to = inp
        break
date_from_obj = datetime.strptime(date_from, '%y%m%d%H%M')
date_to_obj = datetime.strptime(date_to, '%y%m%d%H%M')



def get_tafs(icao, date_from_obj, date_to_obj):
    global proxies_list

    URL = 'http://ogimet.com/display_metars2.php'

    params = {
        'lang': 'en',
        'lugar': icao,
        'tipo': 'FT',
        'ord': 'REV',
        'nil': 'SI',
        'fmt': 'txt',
        'ano': date_from_obj.year,
        'mes': date_from_obj.month,
        'day': date_from_obj.day,
        'hora': date_from_obj.hour,
        'anof': date_to_obj.year,
        'mesf': date_to_obj.month,
        'dayf': date_to_obj.day,
        'horaf': date_to_obj.hour,
        'minf': date_to_obj.minute,
        'send': 'send'
    }

    count = 0

    while (count < 100):
        proxies_list = sorted(proxies_list, reverse=False, key=lambda d: list(d.values()))  # sorting by last used proxy

        proxy = [p for p in proxies_list[0].keys()][0]
        proxies = {
            'http': proxy,
            'https': proxy,
        }
        ts = datetime.timestamp(datetime.now())
        proxies_list[0] = {proxy: ts}
        count = count + 1

        strn = ''
        try:
            response = requests.get(URL, params=params, proxies=proxies, timeout=20)
        # response error handling:
        except Timeout:
            print('Timeout')
            continue
        except requests.exceptions.RequestException as e:
            continue
        except ConnectionResetError:
            continue
        if response.text.strip() == '':
            continue

        try:
            html = BeautifulSoup(response.text, 'html.parser')
            text = html('pre')[0].next.strip()
        except IndexError:
            continue

        if (text.startswith("#Sorry")):
            # Reloop because of Quora limit
            continue

        if (text.find("# No large TAF reports from") > 0 and text.find("# No short TAF reports from") > 0):
            # Reloop because of NO TAF
            strn = ['No TAF for ' + icao + ' in database']
            return strn

        for line in text.splitlines():
            if not line.startswith('#'):
                if line.startswith('                      '):
                    strn = strn + '\t'+ (line).strip() + '\n'
                elif (line.find('=') > 0):
                    strn = strn + (line).strip() + '\n'
                else:
                    strn = strn + (line).strip()

        count = count + 1
        return strn

airports_tafs = dict()

WELCOME_MSG = '''**************************\nTAF FOR '''+str(', '.join(airports))+''' airports for period\n'''+ str(date_from_obj.strftime("%Y-%m-%d %H:%M:%S"))+' - ' + str(date_to_obj.strftime("%Y-%m-%d %H:%M:%S")) +'''\n**************************\n'''

with open("Output.txt", "a") as text_file:
    text_file.truncate(0)
    text_file.write(WELCOME_MSG)
    for index, airport in enumerate(airports):
        print(airport)
        TAF = get_tafs(airport,date_from_obj,date_to_obj)
        airports_tafs[airport] = TAF
        text_file.write(TAF + '\n')

with open('proxies.txt','wb') as proxies_file:
    pickle.dump(proxies_list, proxies_file)

input('Finished.')