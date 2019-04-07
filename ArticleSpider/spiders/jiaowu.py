# -*- coding: utf-8 -*-
import scrapy


class JiaowuSpider(scrapy.Spider):
    name = 'jiaowu'
    allowed_domains = ['']
    start_urls = ['']
    agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0'
    headers = {
    'Host': 'jiaowu.em.swjtu.edu.cn',
     'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Referer':'http://210.41.95.5/',
    'Connection':'keep-alive',
    'User-Agent': agent
}

    def parse(self, response):
        print(response.text)
        pass

    # yield scrapy.Request('', headers=self.headers)
    def start_requests(self):
        captcha_url = ''
        post_data = {
            'url': '',
            'OperatingSystem': '',
            'Browser': '',
            'user_id': '',
            'password': '',
            'ranstring': '',
            'user_type': 'student',
            'btn1': ''
             }
        yield  scrapy.Request(captcha_url,headers=self.headers,meta={'post_data':post_data,'cookiejar':1},callback=self.login_after_captcha)

    def login_after_captcha(self,response):
        login_url = 'http://jiaowu.em.swjtu.edu.cn/servlet/UserLoginSQLAction'
        with open('captcha.jpg', 'wb') as f:
            f.write(response.body)
        from PIL import Image
        img = Image.open('captcha.jpg')
        img.show()
        # img.close()
        captcha = input('请输入验证码\n>>')
        post_data = response.meta['post_data']
        post_data['ranstring'] = captcha
        yield  scrapy.FormRequest(login_url,formdata=post_data,meta={'cookiejar':1},headers = self.headers,callback=self.checkinfo)
        pass

    def checkinfo(self,response):
        print(response.text)
        for url in self.start_urls:
            yield scrapy.Request(url, dont_filter=True, meta={'cookiejar':1},headers=self.headers)
        pass
