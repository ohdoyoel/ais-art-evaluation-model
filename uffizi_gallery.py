# Uffizi Gallery
from bs4 import BeautifulSoup as bs
import requests
import json


def get_page_links(url):
    baseurl = 'https://www.uffizi.it'
    r = requests.get(url)
    sp = bs(r.text, 'html.parser')
    links = sp.select('div.grid__item.tab-6-12.lap-4-12.space--bottom-2 a')
    return [baseurl + link.attrs['href'] for link in links]

def only_artist(s):
    n = s.count('(')
    for j in range(n):
        s = s[:s.find('(')] + s[s.find(')')+2:]
    s = s.strip()
    s = s.replace(u'\xa0', u' ')
    return s


def only_desc(l):
    n = len(l)
    temp = ''
    for j in l:
        temp = temp + ' ' + j.get_text()
    temp = temp.strip()
    temp = temp.replace(u'\xa0', ' ')
    if '    ' in temp:
        temp = temp[:temp.index('    ')]
    return temp

def art_data(url):
    r = requests.get(url)
    sp = bs(r.text, 'html.parser')
    art = {
        'title': sp.select_one('h1.page-heading__title').text.strip().replace('\n', ''),
        'artist': only_artist(sp.select_one('div.page-heading__text').text),
        'img_url': sp.select('div.slider__item img')[0]['src'],
        'desc': only_desc(sp.select('#text > div > div.formatted-content p'))
    }
    return art

result = []

for i in range(1,13):
    url = 'https://www.uffizi.it/en/the-uffizi/painting/artworks?page='+str(i)
    print(i)
    for j in get_page_links(url):
        result.append(art_data(j))

print(result)
print(len(result))


file_path = 'uffizi_paintings.json'
with open(file_path, 'w') as f:
    json.dump(result, f)