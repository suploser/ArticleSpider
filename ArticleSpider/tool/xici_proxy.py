import requests
import MySQLdb
conn = MySQLdb.connect(host='192.168.1.109',user='root',password='123456',database='ArticleSpider',charset='utf8',use_unicode=True)
cursor = conn.cursor()

from scrapy import Selector
url = 'http://www.xicidaili.com/wt/{0}'
ua = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:58.0) Gecko/20100101 Firefox/58.0'
headers = {
    'User-Agent':ua
}
ip_list = []
insert_sql = '''
                     insert into proxy_ips(ip, port, proxy_type) VALUES (%s,%s,%s)
'''
def crawl_ip():
    for i in range(1658):
        response = requests.get(url.format(i+1), headers=headers)
        selector = Selector(text=response.text)#OR (response=response)
        all_tr = selector.css('#ip_list tr')
        for tr in all_tr[1:]:
            all_text = tr.css('td::text').extract()
            ip = all_text[0]
            port =  all_text[1]
            proxy_type = all_text[5]
            ip_list.append((ip,port,proxy_type))

            pass
        for ip_info in ip_list:
            cursor.execute(insert_sql, ip_info)
            conn.commit()
            pass


class GetIP(object):
    def delete_ip (self,ip):
        delete_sql = '''
                   delete   from  proxy_ips  where ip = %s
        '''
        cursor.execute(delete_sql, (ip,))
        conn.commit()
    def jduge_ip(self,ip,port):
        url =' https://www.baidu.com'
        proxy_url = '%s:%s'%(ip,port)
        try:
            response = requests.get(url, proxies={'http':proxy_url})

            if response.status_code >=200 and response.status_code<300:
                return True
            else:
                self.delete_ip(ip)
                return False
        except Exception as e:
            self.delete_ip(ip)
            return False
    def get_ip(self):
        sql = 'select ip, port from proxy_ips order by rand() limit 1'
        cursor.execute(sql)
        for ip_info in cursor.fetchall():
            ip = ip_info[0]
            port = ip_info[1]
            if self.jduge_ip(ip,port):
                return 'http://{0}:{1}'.format(ip,port)
            else:
                return self.get_ip()
# crawl_ip()


# if __name__ == '__main__':
#     print(GetIP().get_ip())