# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from fake_useragent import  UserAgent
from scrapy.http import HtmlResponse
from ArticleSpider.tool.xici_proxy import GetIP
class ArticlespiderSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

class RandomUserAgentMiddleware(object):
    def __init__(self, crawler):
        self.ua = UserAgent()
        self.ua_type = crawler.settings.get('USER_AGENT_TYPE','random')
        pass

    @classmethod
    def  from_crawler(cls,crawler):
        return cls(crawler)

    def process_request(self, request, spider):
        # user_agent = self.ua.random
        # ua_type = self.ua_type
        import os
        import json
        def convert_cookie(cookie_dict):
            cookie_str = ''
            cookie_list=[]
            for k,v in cookie_dict.items():
                cookie_str = str(k)+'='+str(v)
                cookie_list.append(cookie_str)
            return ','.join(cookie_list)
        # print(os.path.dirname(__file__))
        cookie_file = os.path.join(os.path.dirname(__file__), 'spiders/cookies.json')
        cookie_dict = {}
        with open(cookie_file,'r') as f:
            cookie_dict = json.load(f)


        # print(cookie_file)




        c = convert_cookie(cookie_dict)
        # pass

        def get_ua():
            return getattr(self.ua,self.ua_type)
        request.headers.setdefault(b'User-Agent', get_ua())
        request.headers.setdefault(b'Cookie',convert_cookie(cookie_dict))

# class RandomProxyMiddleware(object):
#     def process_request(self,request,spider):
        # gi =  GetIP()
        # random_ip = gi.get_ip()
        # request.meta['proxy'] = 'http://182.141.43.55:9000'


class JsDownloadMiddleware(object):
    def process_request(self, request, spider):
          if spider.name == 'jobbole':
              spider.brower.get(request.url)
              import time
              time.sleep(5)
              print(request.url)
              return HtmlResponse(url=request.url, body=spider.brower.page_source, encoding='utf-8')

