# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import re
from scrapy.loader.processors import MapCompose,TakeFirst,Join
import datetime
from scrapy.loader import ItemLoader
from ArticleSpider.utils.common import extract_num
from ArticleSpider.settings import SQL_DATETIME_FORMAT,SQL_DATE_FORMAT
from w3lib.html import remove_tags


class ArticlespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class ArticlespiderItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


def date_convert(value):
    try:
        created_at = value.strip().replace('·', '').strip()
        return  datetime.datetime.strptime(created_at,'%Y/%m/%d').date()
    except Exception as e:
        return datetime.datetime.now().date()
def get_nums(value):
    match_obj = re.match(r'.*?(\d+).*',value)
    if match_obj:
        num = int(match_obj.group(1))
    else:
        num = 0
    return num
def remove_comment(value):
    if '评论' in value:
        return ''
    else:
        return value
    pass
def return_value(value):
    return value
class JobboleArticleItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    url_obj_id = scrapy.Field()
    content = scrapy.Field()
    tags = scrapy.Field(
        input_processor=MapCompose(remove_comment),
        # input_processor=TakeFirst()
        output_processor = Join(',')
    )
    created_at = scrapy.Field(
        input_processor =MapCompose(date_convert)
    )
    praise_num = scrapy.Field(
        input_processor = MapCompose(get_nums)
    )

    comment_num = scrapy.Field(
        input_processor = MapCompose(get_nums)
    )
    collect_num =scrapy.Field(
        input_processor = MapCompose(get_nums)
         )
    front_img_url = scrapy.Field(
        output_processor = return_value
    )
    front_img_path = scrapy.Field()


class ZhihuQuestionItem(scrapy.Item):
    zhihu_id = scrapy.Field()
    topics = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    answer_num = scrapy.Field()
    comments_num = scrapy.Field()
    click_num = scrapy.Field()
    watch_user_num = scrapy.Field()
    crawl_time = scrapy.Field()
    crawl_update_time = scrapy.Field()
    def get_insert_sql(self):
        insert_sql = '''
                                insert into zhihu_question(zhihu_id,topics,url,content,title,answer_num,comments_num,watch_user_num
                                ,click_num,crawl_time) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE content VALUES
                                (content),comments_num = VALUES (comments_num), answer_num=VALUES (answer_num), watch_user_num
                                =VALUES (watch_user_num),click_num = VALUES (click_num),crawl_update_time = VALUES (crawl_time)
        '''
        zhihu_id = int(''.join(self['zhihu_id']))
        topics = ','.join(self['topics'])
        url = ''.join(self['url'])
        content = ''.join(self['content'])  if self['content'] else 'nothing'
        title = ''.join(self['title'])
        answer_num = extract_num(''.join(self['answer_num']))
        comments_num = extract_num(''.join(self['comments_num']))
        watch_user_num = self['watch_user_num'][0].replace(',','')
        click_num =  self['watch_user_num'][1].replace(',','')
        crawl_time = datetime.datetime.now().strftime(SQL_DATETIME_FORMAT)
        parmas = (zhihu_id,topics,url,content,title,answer_num,comments_num,watch_user_num,click_num,crawl_time)
        return insert_sql,parmas

class ZhihuAnswerItem(scrapy.Item):
    zhihu_id = scrapy.Field()
    url = scrapy.Field()
    question_id = scrapy.Field()
    author_id = scrapy.Field()
    content = scrapy.Field()
    comment_num = scrapy.Field()
    parise_num = scrapy.Field()
    create_time= scrapy.Field()
    update_time = scrapy.Field()
    crawl_time =  scrapy.Field()
    crawl_update_time = scrapy.Field()
    def get_insert_sql(self):
        insert_sql = '''
                                insert into zhihu_answer(zhihu_id, url,question_id,author_id,content,comment_num,parise_num
                                ,create_time,update_time,crawl_time) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE content =VALUES
                                (content),comment_num = VALUES (comment_num), parise_num=VALUES (parise_num), update_time
                                =VALUES (update_time), crawl_update_time = VALUES (crawl_time)
        '''
        zhihu_id = self['zhihu_id']
        url = self['url']
        question_id = self['question_id']
        author_id = self['author_id']
        content = self['content']
        comment_num = self['comment_num']
        parise_num = self['parise_num']
        create_time = datetime.datetime.fromtimestamp(self['create_time']).strftime(SQL_DATETIME_FORMAT)
        update_time = datetime.datetime.fromtimestamp(self['update_time']).strftime(SQL_DATETIME_FORMAT)
        crawl_time = datetime.datetime.now()
        parmas = (zhihu_id, url, question_id, author_id, content, comment_num, parise_num, create_time, update_time, crawl_time)
        return insert_sql, parmas


def remove_splash(value):
    return value.replace('/', '')

def handle_strip(value):
    addr_list = value.split('\n')
    addr_list = [item.strip() for item in addr_list if item.strip()!='查看地图']
    return ''.join(addr_list)


class LagouJobsItemLoader(ItemLoader):
    # pass
    default_output_processor = TakeFirst()


class LagouJobsItem(scrapy.Item):
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    title = scrapy.Field()
    salary = scrapy.Field()
    job_city = scrapy.Field(
        input_processor = MapCompose(remove_splash)
    )
    work_years = scrapy.Field(
        input_processor=MapCompose(remove_splash)
    )
    degree_need = scrapy.Field(
        input_processor=MapCompose(remove_splash)
    )
    job_type = scrapy.Field()
    publish_time = scrapy.Field()
    tags = scrapy.Field(
         output_processor = Join(',')
    )
    job_advantage = scrapy.Field()
    job_desc = scrapy.Field()
    job_addr = scrapy.Field(
        input_processor=MapCompose(remove_tags, handle_strip)
    )
    company_url = scrapy.Field()
    company_name = scrapy.Field()
    crawl_time = scrapy.Field()
    crawl_update_time =scrapy.Field()

    def get_insert_sql(self):
        insert_sql = '''
                             INSERT INTO lagou_jobs(url, url_object_id, title, salary,  job_city, work_years,  degree_need, job_type,
                              publish_time, tags,  job_advantage, job_desc,  job_addr,  company_url, company_name, crawl_time) VALUES 
                              (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE crawl_update_time
                              = VALUES(crawl_time)
        '''

        parma = (self['url'], self['url_object_id'], self['title'], self['salary'], self['job_city'],self['work_years']
                 , self['degree_need'], self['job_type'],self['publish_time'], self['tags'], self['job_advantage'], self['job_desc'],
                 self['job_addr'], self['company_url'], self['company_name'], self['crawl_time']
                 )
        return insert_sql, parma


