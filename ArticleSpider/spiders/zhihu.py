# -*- coding: utf-8 -*-
import scrapy
import re
import json
from urllib import parse
import datetime
from scrapy.loader import ItemLoader
from ArticleSpider.items import ZhihuAnswerItem, ZhihuQuestionItem
class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['https://www.zhihu.com/']
    start_answer_url = '''http://www.zhihu.com/api/v4/questions/{0}/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cupvoted_followees%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics&limit={1}&offset={2}&sort_by=default'''
    agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0'
    _cookies = {
        '_xsrf':'06f4cedc-8f9a-4ce4-931a-bc5a4b7893e1',
        '_zap	':'3ef51f1b-690c-453e-996e-c3c84b138233',
        'aliyungf_tc':'AQAAAHOzlh7pdQIA5Hm6bneOrKrdJgip',
        'capsion_ticket':'"2|1:0|10:1517304855|14:capsion_ticket|44:ZTNjMGFjOTg4NDIwNDJkOGE0ZWYxN'
                         'DdhMTc1YWQ5MzQ=|e6c8447e03ead564ce8df1fe0da4445454041c0598acf09aa25be6a0e95'
                         'ca4eb"',
        'd_c0':'"AJDr1-itEQ2PTnW8TfDxgCDeMFfNY_zYpyM=|1517304739"',
        'q_c1':'95981cd513e64a97ad407ccd7f596065|1517304739000|1517304739000',
        'z_c0':'"2|1:0|10:1517304865|4:z_c0|92:Mi4xUUlNYUJBQUFBQUFBa092WDZLMFJEU1lBQUFCZ0FsVk5'
               'JWXBkV3dDdkcxTjRBVGRPNzE3UkUzVVhnWmpWWDgxTlBn|a247afa41ff0769d0be908f7ee9e56c'
               '3d10e378294d4c08cef08dce1ead296d3"'
    }
    headers = {
        'Host': 'www.zhihu.com',
        'Referer': 'https://www.zhihu.com/',
        'Connection': 'keep-alive',
        'User-Agent': agent
    }

    def parse(self, response):
        all_urls = response.css('a::attr("href")').extract()
        all_urls = [parse.urljoin(response.url,url) for url in all_urls]
        all_urls = filter(lambda  x:True if  x.startswith('https') else False,all_urls)
        for url in all_urls:
            match_obj = re.match(r'(.*zhihu.com/question/(\d+))(/|$).*',url)
            if match_obj:
                request_url = match_obj.group(1)
                question_id = match_obj.group(2)
                yield scrapy.Request(request_url, headers=self.headers, meta={'question_id':question_id}, callback=self.parse_question)
                # break
            else:
                yield scrapy.Request(url, headers=self.headers)
        pass

    def parse_question(self,response):
        question_id = response.meta.get('question_id','')
        item_loader = ItemLoader(item = ZhihuQuestionItem(),response=response)
        item_loader.add_css('title','.QuestionHeader h1.QuestionHeader-title::text')
        item_loader.add_css('topics','.QuestionTopic .Popover  div::text')
        item_loader.add_css('content','.QuestionHeader-detail span::text')
        item_loader.add_value('url',response.url)
        item_loader.add_value('zhihu_id',question_id)
        item_loader.add_css('answer_num','.List-headerText span::text ')
        item_loader.add_css('comments_num','.QuestionHeader-Comment button::text')
        item_loader.add_css('watch_user_num','.NumberBoard-itemValue::text')
        question_item = item_loader.load_item()
        yield scrapy.Request(self.start_answer_url.format(question_id,20,0),headers=self.headers, callback=self.parse_answer)
        yield question_item
        scrapy.FormRequest
        pass
    def parse_answer(self,response):
        asw_json = json.loads(response.text)
        is_end = asw_json['paging']['is_end']
        next_url = asw_json['paging']['next']
        for answer in asw_json['data']:
            answer_item = ZhihuAnswerItem()
            answer_item['zhihu_id'] = answer['id']
            answer_item['url'] = answer['url']
            answer_item['question_id'] = answer['question']['id']
            answer_item['author_id'] = answer['author']['id'] if  id in answer['author'] else None
            answer_item['content'] = answer['content']
            answer_item['comment_num'] = answer['comment_count']
            answer_item['parise_num'] = answer['voteup_count']
            answer_item['create_time'] = answer['created_time']
            answer_item['update_time'] = answer['updated_time']
            answer_item['crawl_time'] = datetime.datetime.now()

            yield answer_item

        if not is_end:
            pass
            yield scrapy.Request(next_url,headers=self.headers,callback=self.parse_answer)

        pass

    def start_requests(self):
        url = 'https://www.zhihu.com'
        yield scrapy.Request(url,headers=self.headers,cookies=self._cookies)

