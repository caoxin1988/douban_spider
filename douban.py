import requests
from pyquery import PyQuery as pq
import json

URL_MAIN = 'https://movie.douban.com/'

def get_hrefs(items):
    dict_href = {}
    for li in items.items():
        data_title = li.attr('data-title')
        href = li.find('li.title a').attr('href')

        if data_title is not None and href is not None:
            dict_href[data_title] = href

    if len(dict_href) != 0:
        text = json.dumps(dict_href, indent=2, ensure_ascii=False)
        with open('data.json', 'w', encoding='utf-8') as f:
            f.write(text)
    
    print(dict_href.__len__())
    return dict_href


def main():
    url = URL_MAIN
    headers = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 \
                        (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36'
    }

    r = requests.get(url=url, headers=headers)

    html = pq(r.text)
    lis = html('#screening .screening-bd .ui-slide-content li.ui-slide-item')

    dict_films = get_hrefs(lis)
    
    for key in dict_films.keys():
        if '碟中谍' in key:
            print(dict_films.get(key))

if __name__ == '__main__':
    main()