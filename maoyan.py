import requests
from pyquery import PyQuery as pq

URL_MAIN = 'https://movie.douban.com/'


def main():
    url = URL_MAIN
    headers = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 \
                        (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36'
    }

    r = requests.get(url=url, headers=headers)

    print(r.text)

if __name__ == '__main__':
    main()