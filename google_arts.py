# Google Arts & Culture
from bs4 import BeautifulSoup as bs
import requests
import json
import time

file_name = 'google_renaissance.html'




def get_page_links(file_name):
    baseurl = 'https://artsandculture.google.com'
    with open(file_name) as f:
        r = f.read()
    sp = bs(r, 'html.parser')
    links = sp.select("div > div > a.e0WtYb.kdYEFe")
    return [baseurl + link.attrs['href'] for link in links]

# just in case
def get_page_links2(file_name):
    baseurl = 'https://artsandculture.google.com'
    with open(file_name) as f:
        r = f.read()
    sp = bs(r, 'html.parser')
    links = sp.select("div > div > a.e0WtYb.kdYEFe.ZEnmnd")
    return [baseurl + link.attrs['href'] for link in links]
# just in case
def get_page_links3(file_name):
    baseurl = 'https://artsandculture.google.com'
    with open(file_name) as f:
        r = f.read()
    sp = bs(r, 'html.parser')
    links = sp.select("div > div > a.e0WtYb.kdYEFe.ZEnmnd.PJLMUc")
    return [baseurl + link.attrs['href'] for link in links]

def get_desc(sp):
    try:
        desc = sp.select_one('section > div.R5VDUc > p').text.replace('\'','').lstrip()
        desc = desc[:desc.find('©')].rstrip()
        return desc
    except:
        return None

def get_title(sp):
    try:
        return sp.select_one('h1.EReoAc').text.strip().replace('\n', '')
    except:
        return None

def get_artist(sp):
    try:
        return sp.select_one('li.XD0Pkb a').text
    except:
        return None

links = get_page_links(file_name)

result = []
for i in range(len(links)):
    result.append('error')

file_path = 'google_arts_renaissance_5060.json'
with open(file_path, 'w') as f:
    json.dump(result, f)

def art_data(links, file_path):
    with open(file_path, "r") as json_file:
        result = json.load(json_file)
    i = 0
    error_ind = []
    for url in links:
        print(i)
        if result[i] == 'error':
            try:
                r = requests.get(url)
                sp = bs(r.text, 'html.parser')
                art = {
                    'title': get_title(sp),
                    'artist': get_artist(sp),
                    #'year': sp.select('li.XD0Pkb')[2].text.replace('Date Created: ',''),
                    'img_url': sp.select_one('img')['src'],
                    'desc': get_desc(sp)
                }
                result[i] = art
                with open(file_path, 'w') as f:
                    json.dump(result, f)
                print(result[i]['title'])
                time.sleep(30)
            except:
                error_ind.append(i)
                print('error')
        i += 1


    if len(error_ind) != 0:
        art_data(links, file_path)

art_data(links, file_path)

