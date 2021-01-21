# def print_hi(name):
#     print(f'Hi, {name}')

import core.source as source
import sources.bilibili.bilibili as bili_source
import requests
import core.url as url

if __name__ == '__main__':
    session = requests.Session()
    url = url.Url(search_url='https://api.bilibili.com/x/web-interface/search/type')
    bilibili = bili_source.BiLiBiLi(name='bilibili', session=session, url=url)
    bilibili.search('星际穿越')
    bilibili.video()