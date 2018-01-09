# -*- coding:utf-8 -*-\
import re
import json
import requests
from lxml import etree
from Queue import Queue
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

class Spider(object):
    def __init__(self):
        self.url = "http://dongwm.com/page/"
        self.headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36"}


        self.queue = Queue()

    def send_response(self, url):
        response = requests.get(url, headers=self.headers)

        response = (response.content).encode('utf-8')
        # response = response.decode('gbk')
        return response

    def make_html(self, html):
        html_obj = etree.HTML(html)
        link_list = html_obj.xpath("//a[@class='post-title-link']/@href")
        for i in link_list:
            self.queue.put(i)

    def make_html_do(self, html):
        # html_obj = etree.HTML(html)
        # 标题
        # tatle = html_obj.xpath('//article[@id="post-wechat-admin：项目设计篇"]//h1/text()')
        # 文章
        # article = html_obj.xpath('//article[@id="post-wechat-admin：项目设计篇"]//text()')
        # str_ = ""
        print html

        pattern2 = re.compile('<h1 class="title">.*</h1>')
        n = pattern2.search(html)
        pattern = re.compile('<div class="post-content" id="post-content" itemprop="postContent">.*</div>', re.DOTALL)
        m = pattern.search(html)

        print m
        return (n.group()+m.group())


    def make_file(self, firl_name, str_html):
        print "正在写入数据..."
        fp = open('./dongweim/'+firl_name + '.html', "w")
        # list_result = list(str_html)
        # list_res = []
        fp.write(str_html)
        fp.close()

    def start_work(self):
        i =2
        while i <= 13:
            html = self.send_response(self.url+str(i))
            self.make_html(html)
            i+=1
        while not self.queue.empty():
            url_p = self.queue.get()
            url_ = "http://dongwm.com" + url_p
            html_ = self.send_response(url_)
            # 使用正则将‘/’去掉

            str_ = self.make_html_do(html_)
            r = re.sub('/', '', url_p)
            self.make_file(r[-6:], str_)

if __name__ == '__main__':
    spider = Spider()
    spider.start_work()