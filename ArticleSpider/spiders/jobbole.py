# -*- coding: utf-8 -*-
import scrapy
import re
import  datetime
from scrapy.http import Request
from urllib import  parse

from  ArticleSpider.items import JobboleArticleItem, ArticlespiderItemLoader
from ArticleSpider.utils.common import  get_md5
from selenium import webdriver
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
# xpath 解析网页
class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts']

    def __init__(self):
        # super(JobboleSpider, self).__init__()
        self.brower = webdriver.Firefox()
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self):
        print('spider closed!')
        self.brower.close()

    def parse(self, response):
        pass
        # post_nodes= response.css('#archive .floated-thumb .post-thumb a')
        # for post_node in post_nodes:
        #     post_url = post_node.css('::attr("href")').extract_first("")
        #     img_url = post_node.css(' img::attr(src)').extract_first("")    #新闻图的地址
        #     yield Request(url=parse.urljoin(response.url, post_url ), meta={'front_img_url':img_url}, callback=self.parse_detail)
        # next_page = response.css('.next.page-numbers::attr(href)').extract_first()
        # if next_page:
        #     yield Request(url=parse.urljoin(response.url,next_page),callback=self.parse)

  #   def parse_detail(self, response):
  #       # 文章标题
  #       title = response.xpath('//div[@class="entry-header"]/h1/text()').extract()[0]
  #       # 文章创建时间
  #       created_at = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/text()').extract()[0].strip().replace('·', '').strip()
  #       # 文章标签
  #       tag_list = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/a/text()').extract()
  #       tag_list = [element for element in tag_list if not element.strip().endswith('评论')]
  #       tags = ','.join(tag_list)
  #       # 获赞数
  #       praise_num = response.xpath('//span[contains(@class,"vote-post-up")]/h10/text()').extract_first()
  #       # 收藏数
  #       collect_num = response.xpath('//span[contains(@class,"bookmark-btn")]/text()').extract()[0]
  #       match_obj = re.match(r'.*?(\d+).*', collect_num)
  #       if match_obj:
  #           collect_num = int(match_obj.group(1))
  #       else:
  #           collect_num = 0
  #           # 评论数
  #       comment_num = response.xpath('//span[contains(@class, "hide-on-480")]/text()').extract()[0]
  #
  #       match_obj = re.match(r'.*?(\d+).*', comment_num)
  #       if match_obj:
  #           comment_num = int(match_obj.group(1))
  #       else:
  #           comment_num = 0
  #       # 内容
  #       scrapy.Selector
  #       content = response.xpath('//div[@class="entry"]').extract()[0]
  #       front_img_url = response.meta.get('front_img_url','')
  #       url_obj_id = get_md5(response.url)
  #
  #       article =  JobboleArticleItem()
  #       article['url_obj_id'] = url_obj_id
  #       article['url'] = response.url
  #       article['front_img_url'] = [front_img_url]
  #       article['title'] = title
  #       #try:
  #       created_at = datetime.datetime.strptime(created_at,'%Y/%m/%d').date()
  #       article['created_at']=created_at
  #       article['url'] = response.url
  #       article['tags'] = tags
  #       article['content'] = content
  #       article['praise_num'] = praise_num
  #       article['collect_num'] = collect_num
  #       article['comment_num'] = comment_num
  #
  # # ItemLoader加载item
  #       item_loader = ArticlespiderItemLoader(item = JobboleArticleItem(),response = response)
  #       item_loader.add_xpath('title','//div[@class="entry-header"]/h1/text()')
  #       item_loader.add_xpath('created_at','//p[@class="entry-meta-hide-on-mobile"]/text()')
  #       item_loader.add_xpath('tags','//p[@class="entry-meta-hide-on-mobile"]/a/text()')
  #       item_loader.add_xpath('praise_num','//span[contains(@class,"vote-post-up")]/h10/text()')
  #       item_loader.add_xpath('collect_num','//span[contains(@class,"bookmark-btn")]/text()')
  #       item_loader.add_xpath('comment_num','//span[contains(@class, "hide-on-480")]/text()')
  #       item_loader.add_value('url',response.url)
  #       item_loader.add_value('url_obj_id',get_md5(response.url))
  #       item_loader.add_value('front_img_url',[response.meta.get('front_img_url','')])
  #       item_loader.add_xpath('content','//div[@class="entry"]')
  #       article_item = item_loader.load_item()
  #
  #       yield article_item
  #
  #       pass







