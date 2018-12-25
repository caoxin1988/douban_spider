import requests

import common

def login(user_name, pass_word):
    data = {
        'source' : 'movie',
        'redir' : 'https://movie.douban.com/',
        'login' : '登录',
        'form_email' : user_name,
        'form_password' : pass_word,
        'captcha-solution' : 'solid',
        'captcha-id' : 'oFIFx1czAGo0lyqwhhrCiYRC:en'
    }

    s = requests.session()
    response = s.post(url = common.LOGIN_URL, data = data, headers = common.HEADERS)
    print(response.text)
    print(response.cookies)

if __name__ == '__main__':
    login(user_name = common.USER_NAME, pass_word = common.PASS_WORD)