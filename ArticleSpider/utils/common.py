import hashlib
import re

def get_md5(url):
    if isinstance(url,str):
        url = url.encode('utf-8')
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()

def extract_num(text):
    match_obj = re.match(r'.*?(\d+).*', text)
    if match_obj:
        num = int(match_obj.group(1))

    else:
        num = 0
    return

def get_cookies():
    from selenium import webdriver
    brower = webdriver.Firefox()
    brower.get(' https://passport.lagou.com/login/login.html')
    brower.find_element_by_css_selector('input[placeholder="请输入常用手机号/邮箱"]').send_keys('18728899376')
    brower.find_element_by_css_selector('input[placeholder="请输入密码"]').send_keys('1321131987')
    brower.find_element_by_css_selector('input.btn.btn_green.btn_active.btn_block.btn_lg').click()
    import time
    import json
    time.sleep(10)
    Cookies = brower.get_cookies()
    # print(Cookies)
    cookie_dict = {}
    with open('cookies.json', 'w') as f:
        for cookie in Cookies:
            cookie_dict[cookie['name']] = cookie['value']
        json.dump(cookie_dict, f)
    brower.close()

if __name__ == "__main__":
    get_cookies()
#     print(get_md5('https://www.youjizz.com'))
