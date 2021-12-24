
import json
import requests
url = "https://bing-news-search1.p.rapidapi.com/news"

querystring = {"safeSearch": "Off", "textFormat": "Raw"}

headers = {
    'x-bingapis-sdk': "true",
    'x-rapidapi-key': "e2f9480afemsh3384d03efb08d14p103f6ejsn0e4ed40bbbb4",
    'x-rapidapi-host': "bing-news-search1.p.rapidapi.com"
    }

from bs4 import BeautifulSoup as BSHTML
from html2markdown import convert

# TODO catch exceptions
response = requests.request("GET", url, headers=headers, params=querystring)
news_json = json.loads(response.text)

if news_json.get('value'):
    for news_item in news_json['value']:
        # {
        # '_type': 'NewsArticle',
        # 'name': 'Angela Merkel: Letzte Gelegenheit für die Hauptstadtpresse',
        # 'url': 'https://www.msn.com/de-de/nachrichten/politik/angela-merkel-letzte-gelegenheit-f%C3%BCr-die-hauptstadtpresse/ar-AAMq8Og',
        # 'image': {'_type': 'ImageObject', 'thumbnail': {'_type': 'ImageObject', 'contentUrl': 'https://www.bing.com/th?id=OVFT.lERKVrGa9FkH_xRNA9sRqC&pid=News', 'width': 600, 'height': 315},
        # 'isLicensed': True},
        # 'description': 'Die Sommer-Pressekonferenzen der Kanzlerin sind Kult. Sie leben von ihrem spröden Humor und spiegeln die Stimmung im Land. An diesem Mittwoch dürfen Merkel zum letzten Mal Fragen gestellt werden',
        # 'provider': [{'_type': 'Organization', 'name': 'SZ.de', 'image': {'_type': 'ImageObject', 'thumbnail': {'_type': 'ImageObject', 'contentUrl': 'https://www.bing.com/th?id=ODF.ljVx36peutQJEGpk199slg&pid=news'}}}],
        # 'datePublished': '2021-07-22T07:52:00.0000000Z'}
        print('-------------------------------------')
        print(news_item)
        # x = ''
        # print('---------------------------------------------------------------------------------')
        # print('---------------------------------------------------------------------------------')
        # print('---------------------------------------------------------------------------------')
        # # TODO catch exceptions
        # r = requests.get(news_item['url'])
        # print(r.text)
        # print('---------------------------------------------------------------------------------')
        # print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
        # s = BSHTML(r.text, 'html.parser')
        # p_list = s.find_all('p')
        # for i in p_list:
        #     x += i.text
        # print(convert(x))


