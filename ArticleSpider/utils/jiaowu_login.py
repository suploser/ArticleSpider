# -*- coding:utf-8 -*-
import requests
# import http.cookiejar as  cookiejar
import json
# import re

login_url = 'http://jiaowu.em.swjtu.edu.cn/servlet/UserLoginSQLAction'
session = requests.session()
# session.cookies = cookiejar.LWPCookieJar(filename='cookie.txt')
url = 'http://jiaowu.em.swjtu.edu.cn/'
# try:
#     session.cookies.load(filename='cookies.txt',ignore_discard=True)
# except:
#     print('未能加载cookies')
agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0'
header = {
    'Host': 'jiaowu.em.swjtu.edu.cn',
     'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Referer':'http://210.41.95.5/service/login.jsp?user_type=student',
    'Connection':'keep-alive',
    'User-Agent': agent
}
captcha_url = 'http://jiaowu.em.swjtu.edu.cn/servlet/GetRandomNumberToJPEG'
index_url = 'http://jiaowu.em.swjtu.edu.cn/usersys/index.jsp'


def get_sessionid():
    response = session.get(url,headers=header)
    # print(response.cookies)
    _cookie = requests.utils.dict_from_cookiejar(response.cookies)
    return _cookie
    pass



def get_captcha():
    response = session.get(captcha_url, headers=header)
    with open('captcha.jpg', 'wb') as f:
        f.write(response.content)
    from PIL import Image
    img = Image.open('captcha.jpg')
    img.show()

    captcha = input('请输入验证码\n>>')

    return captcha


def get_index(cookies):

    response = requests.get(index_url,headers=header,cookies=cookies, allow_redirects=False)
    print(response.text)
    pass


def jiaowu_login(stu_id, password):
    # get_sessionId()
    # global  _cookie

    _cookie=get_sessionid()
    post_data = {
        'url':'http://jiaowu.em.swjtu.edu.cn/servlet/UserLoginCheckInfoAction',
        'OperatingSystem':'',
        'Browser':'',
        'user_id':stu_id,
        'password': password,
        'ranstring': get_captcha(),
        'user_type':'student',
        'btn1':''
    }

    response = session.post(login_url, data=post_data, headers=header)
    # print(response.cookies)
    print(response.text)
    cookies = requests.utils.dict_from_cookiejar(response.cookies)

    cookies.update(_cookie)

    # session.cookies.save()
    f = open('cookie.json','w')
    json.dump(cookies,f)
    f.close()

# get_sessionId()


jiaowu_login('2014121829','******')
# with open('cookie.json','r') as f:
#     cookies = json.load(f)
# get_index(cookies)
# # get_sessionid()



