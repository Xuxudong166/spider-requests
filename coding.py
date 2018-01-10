# -*- coding:utf-8 -*-\
import re

import requests
from lxml import etree
from Queue import Queue
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

class Spider(object):
    def __init__(self):
        self.url = "http://codingpy.com/page/"
        self.headers = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                        'Accept-Encoding':'gzip, deflate',
                        'Accept-Language':'zh-CN,zh;q=0.8',
                        'Connection':'keep-alive',
                        'Cookie':'_ga=GA1.2.769272104.1515306687; Hm_lvt_1a54d19172d7819c009872071839bfe3=1515306690,1515417813,1515571944; Hm_lpvt_1a54d19172d7819c009872071839bfe3=1515575274',
                        'Host':'codingpy.com',
                        'If-Modified-Since':'Mon, 08 Jan 2018 13:20:00 GMT',
                        'Upgrade-Insecure-Requests':'1',
                        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}

        self.queue = Queue()

    def send_response(self, url):
        response = requests.get(url, headers=self.headers)

        response = (response.content).encode('utf-8')
        # response = response.decode('gbk')
        return response

    def make_html(self, html):
        try:
            html_obj = etree.HTML(html)
            link_list = html_obj.xpath('//div[@class="header"]/a/@href')
            print link_list
            for i in link_list:
                self.queue.put(i)
        except Exception, e:
            print e

    def make_html_do(self, html):

        # time.sleep(5)
        try:
            pattern2 = re.compile('<div class="article">.*分享到微信', re.DOTALL)
            n = pattern2.search(html)


            # print n.group()
            return n.group()
        except Exception, e:
            print e


    def make_file(self, firl_name, str_html):
        try:
            print "正在写入数据..."
            fp = open('./dongweim/'+firl_name + '.html', "w")
            # list_result = list(str_html)
            # list_res = []
            fp.seek(0)
            fp.write(str_html)
            fp.close()
        except Exception, e:
            print e

    def start_work(self):
        i = 1
        while i <= 21:
            print i
            html = self.send_response(self.url+str(i))
            # print html
            self.make_html(html)
            i+=1
        while not self.queue.empty():
            url_p = self.queue.get()

            html_ = self.send_response(url_p)
            # 使用正则将‘/’去掉
            # print html_
            str_ = self.make_html_do(html_)
            r = re.sub('/', '', url_p)
            self.make_file(r[-6:], str_)

if __name__ == '__main__':
    spider = Spider()
    spider.start_work()