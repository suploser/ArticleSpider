# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ArticleSpider.utils.common import  get_md5
from ArticleSpider.items import LagouJobsItem,LagouJobsItemLoader
import datetime
class LagouSpider(CrawlSpider):
    name = 'lagou'
    allowed_domains = ['www.lagou.com']
    start_urls = ['https://www.lagou.com/']
    custom_settings = {
        'COOKIES_ENABLED': False,
        'DOWNLOAD_DELAY':3,
        'DOWNLOADER_MIDDLEWARES':{
            'ArticleSpider.middlewares.RandomUserAgentMiddleware':1,
        },
    #     'ITEM_PIPELINES': {
    #     # 'ArticleSpider.pipelines.ArticlespiderPipeline': 300,
    #     # 'ArticleSpider.pipelines.JsonWithEncodingPipeline':299,
    #     # 'ArticleSpider.pipelines.ArticleImagePipleline': 298,
    #     'ArticleSpider.pipelines.MysqlTwistedPipeline':1,
    # },
        'DEFAULT_REQUEST_HEADERS':{
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Connection': 'keep-alive',
            'Host': 'www.lagou.com',
            'Origin': 'https://www.lagou.com',
            'Referer': 'https://www.lagou.com/',
        }
    }

    rules = (
        Rule(LinkExtractor(allow='jobs/\d+.html'),follow=True, callback='parse_job'),
        Rule(LinkExtractor(allow='zhaopin/.*'),),
        Rule(LinkExtractor(allow='gongsi/\d+.html'))
    )


    def parse_job(self, response):
        pass
        # i = {}
        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
        # item_loader = LagouJobsItemLoader(item=LagouJobsItem(), response=response)
        # item_loader.add_value('url',response.url)
        # item_loader.add_value('url_object_id',get_md5(response.url))
        # item_loader.add_css('title','.job-name span::text')
        # item_loader.add_css('salary','.job_request .salary::text')
        # item_loader.add_xpath('job_city','//*[@class="job_request"]/p/span[2]/text()')
        # item_loader.add_xpath('work_years','//*[@class="job_request"]/p/span[3]/text()')
        # item_loader.add_xpath('degree_need','//*[@class="job_request"]/p/span[4]/text()')
        # item_loader.add_xpath('job_type','//*[@class="job_request"]/p/span[5]/text()')
        # item_loader.add_css('publish_time','.publish_time::text')
        # item_loader.add_css('tags','.position-label li::text')
        # item_loader.add_css('job_advantage','.job-advantage p::text')
        # item_loader.add_css('job_desc','.job_bt div')
        # item_loader.add_css('job_addr','.work_addr')
        # item_loader.add_css('company_url','#job_company a::attr(href)')
        # item_loader.add_css('company_name', '#job_company a img::attr(alt)')
        # item_loader.add_value('crawl_time', datetime.datetime.now())
        # item = item_loader.load_item()
        #
        # return item
