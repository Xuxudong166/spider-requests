# -*- coding:utf-8 -*-\
import urllib
import urllib2
import requests
from lxml import etree
import random
import time
import os
from Queue import Queue
from multiprocessing.dummy import Pool

class XinlangNews(object):

    def __init__(self):
        self.url = "http://news.sina.com.cn/china/"
        self.proxy_list = [{}, {}]
        self.USER_AGENT_LIST = [
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
            "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/531.21.8 (KHTML, like Gecko) Version/4.0.4 Safari/531.21.10",
            "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/533.17.8 (KHTML, like Gecko) Version/5.0.1 Safari/533.17.8",
            "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5",
            "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-GB; rv:1.9.1.17) Gecko/20110123 (like Firefox/3.x) SeaMonkey/2.0.12",
            "Mozilla/5.0 (Windows NT 5.2; rv:10.0.1) Gecko/20100101 Firefox/10.0.1 SeaMonkey/2.7.1",
            "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_8; en-US) AppleWebKit/532.8 (KHTML, like Gecko) Chrome/4.0.302.2 Safari/532.8",
            "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.464.0 Safari/534.3",
            "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_5; en-US) AppleWebKit/534.13 (KHTML, like Gecko) Chrome/9.0.597.15 Safari/534.13",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_2) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.186 Safari/535.1",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.874.54 Safari/535.2",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7",
            "Mozilla/5.0 (Macintosh; U; Mac OS X Mach-O; en-US; rv:2.0a) Gecko/20040614 Firefox/3.0.0 ",
            "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.0.3) Gecko/2008092414 Firefox/3.0.3",
            "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; en-US; rv:1.9.1) Gecko/20090624 Firefox/3.5",
            "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; en-US; rv:1.9.2.14) Gecko/20110218 AlexaToolbar/alxf-2.0 Firefox/3.6.14",
            "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1"
        ]
        self.headers = {"User-Agent" : random.choice(self.USER_AGENT_LIST), 'referer':"http://news.sina.com.cn"}
        # self.request = Queue()
    # os.makedirs()
    # 创建目录的命令
    # open

    def send_request(self, url):
        try:
            response = requests.get(url, headers=self.headers, proxies = random.choice(self.proxy_list), timeout=5)
            return response.content
        except Exception, e:
            print "[INFO]拉取网页错误%s"%e



    def mk_txt(self, file_name, html):
        """创建文件"""
        try:

            if not os.path.exists(file_name):
                with open(file_name+'.txt', 'w') as m:
                    m.write(html)
        except Exception, e:
            print '[INFO]创建文件错误%s'%e



    def mk_dir(self, name):
        """创建文件夹方法"""
        # 判断是否存在文件夹
        if not os.path.exists(name):
            os.makedirs(name)


    def first_name(self, html):
        """大类查找"""

        try:
            html_obj = etree.HTML(html)
            name_list = html_obj.xpath("//div[@class='wrap']/a/text()")
            test_result = []
            for text_html in name_list:
                # print type(text_html)
                test_result.append(text_html.strip().encode('utf-8'))
            # 取到国内、国际、社会三个大类名字
            name = test_result[1:4]
            href_list = html_obj.xpath("//div[@class='wrap']/a/@href")
            # 取到链接
            href = href_list[1:4]
            # 组合成一个大列表
            item = zip(name, href)
            return item
        except Exception, e:
            print '[INFO]大类返回错误%s'%e



    def secoend_name(self, html):
        """中类查找"""
        try:
            html_obj = etree.HTML(html)
            name_list = html_obj.xpath('//div[@class="links"]/a/text()')
            test_result = []
            for text_html in name_list:
                # print type(text_html)
                test_result.append(text_html.strip().encode('utf-8'))

            href_list = html_obj.xpath("//div[@class='links']/a/@href")
            # 取到链接
            # 组合成一个大列表
            item = zip(test_result, href_list)
            return item
        except Exception, e:
            print '中类查找错误%s'%e

    def third_name(self, html):
        """小类查找"""
        try:
            html_obj = etree.HTML(html)
            name_list = html_obj.xpath('//ul[@class="list_009"]/li/a/text()')
            test_result = []
            for text_html in name_list:
                # print type(text_html)
                test_result.append(text_html.strip().encode('utf-8'))

            href_list = html_obj.xpath('//ul[@class="list_009"]/li/a/@href')
            # 取到链接
            # 组合成一个大列表
            item = zip(test_result, href_list)
            return item
        except Exception, e:
            print '[INFO]小类查找错误%s'%e

    def some_html(self, html):
        """文章"""
        try:
            html_obj = etree.HTML(html)
            text = html_obj.xpath("//div[@class='article']/p/text()")
            test_result = ''
            for text_html in text:
                # print type(text_html)
                test_result += (text_html.strip().encode('utf-8')+'\n')

            return test_result
        except Exception, e:
            print '[INFO]文章返回错误%s'%e


    def start_work(self):
        # 首页的内容
        html_first = self.send_request(self.url)
        # 拿到一个包含大类和对应链接的列表
        list_first = self.first_name(html_first)


        # 遍历列表
        for i in list_first:
            # 创建文件夹
            self.mk_dir(i[0])

            # 拿到大类的页面内容
            html_big = self.send_request(i[1])
            # 拿到一个包含中类和对应链接的列表
            list_secoend = self.secoend_name(html_big)

            for o in list_secoend:
                # 创建文件夹
                self.mk_dir((i[0] + '/' + o[0]))

                # 拿到中类的页面内容
                html_mid = self.send_request(o[1])

                # 拿到一个包含小类和对应链接的列表
                list_third = self.third_name(html_mid)

                # 遍历小类列表
                for p in list_third:
                    # 拿到详情页数据
                    html_text = self.send_request(p[1])
                    text = self.some_html(html_text)
                    self.mk_txt((i[0] + '/' + o[0] + '/' + p[0]), text)





if __name__ == '__main__':
    start = time.time()
    spider = XinlangNews()
    spider.start_work()
    endtime = time.time()
    print endtime-start
