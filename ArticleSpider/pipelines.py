# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
#异步模块
from twisted.enterprise import adbapi

import json
import  codecs
import  MySQLdb
import MySQLdb.cursors
class ArticlespiderPipeline(object):
    def process_item(self, item, spider):
        return item
class JsonWithEncodingPipeline(object):
    def __init__(self):
        self.file = codecs.open('article.json','w',encoding='utf-8')
    def process_item(self,item,spider):
        line = json.dumps(dict(item),ensure_ascii=False)+"\n"
        self.file.write(line)
        return item
    # 爬虫结束后调用
    #   信号量
    # def spider_closed(self,spider):
    #     self.file.close()
# 同步方式写入数据库
class  MysqlPipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect(host='192.168.1.109',user='root',password='123456',database='ArticleSpider',charset='utf8',use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        sql = ''
        self.cursor.execute(sql, (item['title'],item['url'],item['created_at'],item['collect_num']))
        self.conn.commit()

#异步方式写入数据库
class MysqlTwistedPipeline(object):
    def __init__(self,dbpool):
        self.dbpool = dbpool

    @classmethod
    def  from_settings(cls,settings):
       dbparms=dict (
                            host = settings['MYSQL_HOST'],
                            password = settings['MYSQL_PASSWORD'],
                            user = settings['MYSQL_USER'],
                            database = settings['MYSQL_DATABASE'] ,
                            cursorclass = MySQLdb.cursors.DictCursor,
                            charset = 'utf8',
                            use_unicode = True,
        )
       dbpool = adbapi.ConnectionPool('MySQLdb', **dbparms)
       return  cls(dbpool)

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self.do_insert,item)
        query.addErrback(self.err_handler, item, spider)

    def do_insert(self,cursor,item):
         insert_sql, parmas = item.get_insert_sql()
         print(insert_sql, parmas)
         cursor.execute(insert_sql, parmas)
         pass



    def err_handler(self,failure, item, spider):
        print(failure)


class ArticleImagePipleline(ImagesPipeline):
    def item_completed(self, results, item, info):
        for ok,value in results:
            img_path = value['path']
        item['front_img_path'] = img_path
        return item
        pass
