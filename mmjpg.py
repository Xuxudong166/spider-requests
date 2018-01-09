# -*- coding:utf-8 -*-\
import requests
from lxml import etree
import time
import random

class ZhaiNan(object):
    def __init__(self):
        self.before_url = 'http://www.mm131.com/xinggan/list_6_'
        self.proxy_list = [{"http": "mr_mao_hacker:sffqry9r@120.27.218.32:16816"}, {}]
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
        self.headers = {"User-Agent" : random.choice(self.USER_AGENT_LIST),'referer':"http://www.mm131.com/"}


    def get_response(self, url):

        response = requests.get(url, headers = self.headers, proxies = random.choice(self.proxy_list))
        return response.content

    def load_page(self, html):
        html_obj = etree.HTML(html)
        link_list = html_obj.xpath("//dl[@class='list-left public-box']/dd/a[@target='_blank']/@href")
        return link_list

    def load_image(self, html):
        html_obj = etree.HTML(html)
        link_list = html_obj.xpath("//div[@class='content-pic']/a/img/@src")

        return link_list

    def write_img(self, data, file_name):
        print "正在写入...%s"%file_name
        with open('./img/' + file_name, 'wb') as f:
            f.write(data)

    def next_url(self, html):
        html_obj = etree.HTML(html)
        link_list = html_obj.xpath('//a[@class="page-ch"][last()]/@href')
        return link_list

    def next_page(self, url):

        # 拿到图片详情页面数据
        html_page = self.get_response(url)

        # 得到图片的地址
        url_page = self.load_image(html_page)

        img = None
        # 得到图片的信息
        try:
            img = self.get_response(url_page[0])
        except:
            pass

        num = random.randint(0, 100)
        # 写入图片
        try:
            self.write_img(img, str(num)+url_page[0][-5:])
        except:
            pass

        # 拿到下一页的链接
        next_url = self.next_url(html_page)
        return next_url

    def start_work(self):

        for page in range(1, 11):

            url_first = self.before_url + str(page) + '.html'
            # 得到首页的数据
            html = self.get_response(url_first)
            # 得到图片详情页的链接列表
            url_list = self.load_page(html)


            for url in url_list:
                time.sleep(1)

                # 拿到图片详情页面数据
                # html_page = self.get_response(url)
                #
                # # 得到图片的地址
                # url_page = self.load_image(html_page)
                #
                # # 得到图片的信息
                # img = self.get_response(url_page)
                # # 写入图片
                # self.write_img(img, url_page[-7:])
                #
                # # 拿到下一页的链接
                # next_url = self.next_url(html_page)
                # 得到下一页的链接
                next_url = self.next_page(url)
                print next_url
                while 1:
                    next_url_new = self.next_url('http://www.mm131.com/xinggan/' + str(next_url))
                    if not next_url_new:
                        print "这位姑娘爬完了"
                        break
                    else:
                        next_url = next_url_new


if __name__ == '__main__':
    spider = ZhaiNan()
    spider.start_work()