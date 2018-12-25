import requests
from pyquery import PyQuery as pq
import json
import re
import sys
import csv

from FilmId import FilmId
import common

'''
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
'''

def get_comment_page(film_id):
    film_id += '/'
    url = common.URL_MAIN + common.DOUBAN_SUBJECT + film_id
    params = {
        'from' : 'showing'
    }

    response = requests.get(url=url, params=params, headers=common.HEADERS)
    with open('test.txt', 'w', encoding='utf-8') as f:
        f.write(response.text)

    doc = pq(response.text)
    html = doc('.article #comments-section #hot-comments a')

    count = 0
    for item in html.items():
        if item.attr('href').startswith('comments'):
            pattern = re.compile('comments.*sort=(?P<sort>.*?)&.*status=(?P<status>.*)$')
            res = re.match(pattern, item.attr('href'))
            params = res.groupdict()

            pattern = re.compile('\d+')
            res = re.findall(pattern, item.text())
            if res:
                count = res[0]
            break

    return film_id, params, count

def get_comment_percent(doc : pq):
    '''
    get comment percent for target film
    '''

    html = doc('.comment-filter')
    comment_name = html.find('.filter-name').text().split(' ')[1:]
    comment_percent = html.find('.comment-percent').text().split(' ')[1:]

    print(comment_name, comment_percent)


def get_comment_content(doc : pq, csv_writer):
    '''
    get comment content for target film
    '''
    comments = doc('.comment')
    for comment in comments.items():
        votes = comment('.votes').text()
        user_name = comment('.comment-info a').text()
        content = comment('.short').text()
        
        csv_writer.writerow([user_name, votes, content])

def get_comments(film_id, param, csv_writer):

    film_id += '/'
    url = common.URL_MAIN + common.DOUBAN_SUBJECT + film_id + common.DOUBAN_COMMENTS
    response = requests.get(url=url, params=param, headers=common.HEADERS)

    doc = None
    if 'start' in param:
        html = json.loads(response.text)['html']
        doc = pq(html)
    else:
        doc = pq(response.content)

    if 'start' not in param:
        get_comment_percent(doc)

    get_comment_content(doc, csv_writer)

def main():
    file_id, param, comment_count = get_comment_page(FilmId.PADMAN.value)

    with open(common.RESULT_FILE, 'w', encoding='utf-8') as f:
        csv_writer = csv.writer(f)

        for i in range(int(comment_count) // 20 + 1):
            print(i)
            if i == 0:
                get_comments(file_id, param, csv_writer)
            else:
                param['start'] = str(i * 20)
                param['limit'] = '20'
                param['comments_only'] = '1'
                get_comments(file_id, param, csv_writer)

if __name__ == '__main__':
    main()