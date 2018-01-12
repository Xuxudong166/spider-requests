# -*- coding:utf-8 -*-\
import requests
import csv
from lxml import etree
import time
from Queue import Queue
import sys
import threading
reload(sys)
sys.setdefaultencoding("utf-8")

class Huangye(object):
    def __init__(self):
        self.before_url = 'http://www.huangye88.com/search.html?kw=%E5%8C%97%E4%BA%AC%E5%9F%B9%E8%AE%AD%E5%85%AC%E5%8F%B8&type=company&page='
        self.proxy = {"https": "https://101.68.73.54:53281"}
        self.headers = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                        'Accept-Encoding':'gzip, deflate',
                        'Accept-Language':'zh-CN,zh;q=0.8',
                        'Cache-Control':'max-age=0',
                        'Connection':'keep-alive',
                        'Content-Length':'105',
                        'Content-Type':'application/x-www-form-urlencoded',
                        'Cookie':'PHPSESSID=b2a4956a38164224aed5cb0aac982dfc5a52293a41ddd6.56433895; hy88showeditems=a%3A3%3A%7Bi%3A14531971%3Ba%3A2%3A%7Bs%3A7%3A%22subject%22%3Bs%3A18%3A%22%E5%8C%97%E4%BA%AC%E5%9F%B9%E8%AE%AD%E5%9F%BA%E5%9C%B0%22%3Bs%3A3%3A%22url%22%3Bs%3A47%3A%22http%3A%2F%2Fjiaoyu.huangye88.com%2Fxinxi%2F14531971.html%22%3B%7Di%3A111368106%3Ba%3A2%3A%7Bs%3A7%3A%22subject%22%3Bs%3A72%3A%2212%E7%B1%B3%E5%8D%87%E9%99%8D%E5%B9%B3%E5%8F%B0%E8%BD%A614%E7%B1%B3%E9%AB%98%E7%A9%BA%E4%BD%9C%E4%B8%9A%E8%BD%A616%E7%B1%B3%E9%AB%98%E7%A9%BA%E4%BD%9C%E4%B8%9A%E8%BD%A6%E5%8E%82%E5%AE%B6%E4%BB%B7%E6%A0%BC%22%3Bs%3A3%3A%22url%22%3Bs%3A47%3A%22http%3A%2F%2Fqiche.huangye88.com%2Fxinxi%2F111368106.html%22%3B%7Di%3A42300167%3Ba%3A2%3A%7Bs%3A7%3A%22subject%22%3Bs%3A51%3A%22%E7%A2%B3%E4%BA%A4%E6%98%93%E5%8C%97%E4%BA%AC%E5%9F%B9%E8%AE%AD%E7%A2%B3%E5%AE%A1%E8%AE%A1%E5%B8%88%E5%9F%B9%E8%AE%AD%E8%81%94%E7%B3%BB%E6%9E%97%E7%90%B3%22%3Bs%3A3%3A%22url%22%3Bs%3A45%3A%22http%3A%2F%2Ffuwu.huangye88.com%2Fxinxi%2F42300167.html%22%3B%7D%7D; gr_user_id=452fa9ee-251b-4fa0-954f-e153bf14927a; _ga=GA1.2.534025655.1515333947; _gid=GA1.2.1799786070.1515333947; _gat=1; Hm_lvt_c8184fd80a083199b0e82cc431ab6740=1515333947,1515333962,1515333979,1515396646; Hm_lpvt_c8184fd80a083199b0e82cc431ab6740=1515398205',
                        'Host':'www.huangye88.com',
                        'Origin':'http://www.huangye88.com',
                        'Referer':'http://www.huangye88.com/search.html?kw=%E5%8C%97%E4%BA%AC%E5%9F%B9%E8%AE%AD%E5%85%AC%E5%8F%B8&type=company',
                        'Upgrade-Insecure-Requests':'1',
                        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}

        self.headers_2 = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}

        self.formdata = {
                        'kw':'北京培训公司',
                        'cattrace':'',
                        'type':'company',
                        'pagetype':'13',
                        'a':'0',
                        'c':'0',
                        'uu':'1'
                        }
        self.list_1 = Queue()
        self.list_ = Queue()
        self.list_2 = Queue()
        # self.list_compy = []
        self.fp = file('huangye.csv', "a")
        self.csv_writer = csv.writer(self.fp)
        item = {"公司名":"", "地址":"", "产品":"", "联系人":""," 电话":""}
        sheet = item.keys()
        self.csv_writer.writerow(sheet)




    def send_request(self, url):

        try:
            response = requests.post(url=url, data=self.formdata, headers=self.headers, proxies=self.proxy, timeout=10)
            a = response.text
            b = a.encode('utf-8')
            # print b
            # return b
            # self.list_1.put(b)
            self.make_html(b)
        except:
            try:
                response = requests.post(url=url, data=self.formdata, headers=self.headers, proxies=self.proxy, timeout=10)
                a = response.text
                b = a.encode('utf-8')
                # print b
                self.make_html(b)
            except Exception,e:
                print e
    def send_response(self, url):
        try:
            response = requests.get(url=url, headers=self.headers_2, proxies=self.proxy, timeout=10)
            a = (response.content).encoding("utf-8")

            # print b
            self.nake_html_nake(a)
        except:
            try:
                response = requests.get(url=url, headers=self.headers_2, proxies=self.proxy, timeout=10)
                a = response.content

                # print b
                self.nake_html_nake(a)
            except Exception,e:
                print e

    def make_html(self, html):
        try:
            html_obj = etree.HTML(html)
            html_txt = html_obj.xpath("//li[@class='wap']//a[@target='_blank']/@href")
            for i in html_txt:
                self.list_.put(i)
        except Exception, e:
            print e

    def nake_html_nake(self, html):
        try:
            print '开始分析详情页'
            html_obj = etree.HTML(html)
            # 公司名
            compty_name = html_obj.xpath("//h1/text()")
            # 地址
            compty_adr = html_obj.xpath("//ul[@class='l-txt']/li[last()]/a/text()")
            # 产品
            compty_product = html_obj.xpath("//div[@class='l-content']/ul[2]/li[last()-1]/text()")
            # 联系人
            compty_contact = html_obj.xpath("//div[@class='c-left']/div[3]/div/ul[@class='l-txt none']/li[1]/a/text()")
            # 电话
            compty_phone = html_obj.xpath("//div[@class='c-left']/div[3]/div/ul[@class='l-txt none']/li[4]/text()")

            print compty_name[0],compty_adr[0], compty_product[0][5:], compty_contact[0], compty_phone[0]

            item = {}
            item["公司名"] = compty_name[0]
            item["地址"] = compty_adr[0]
            item["产品"] = compty_product[0][5:]
            item["联系人"] = compty_contact[0]
            item["电话"] = compty_phone[0]
            # item = dict(item)

            # item = item.encoding("utf-8")
            self.json_list(item)

        except Exception, e:
            print e

    def json_list(self, item):
        print "正在写入数据..."

        # while not self.list_2.empty():
        #     list_2 = self.list_2.get()
        data = item.values()
        # print data
        # list_result = list(list_2)

        # print list_res[0]
        # list_result.append(list_2)
        self.csv_writer.writerow(data)
        # json.dump(list_result, self.fp)

        print "写入完成"



    def start_work(self):
        thread_list = []
        list_0 = [i for i in range(1, 250)]
        for url in list_0:
            thread = threading.Thread(target=self.send_request, args=[self.before_url+str(url)])
            thread.start()
            thread_list.append(thread)
            # self.send_request(self.before_url+str(url))
        for thread in thread_list:
            thread.join()
        # while not self.list_1.empty():
        #     html = self.list_1.get()
        #     self.make_html(html)


        thread_list_2 = []
        while not self.list_.empty():
            url_make = self.list_.get()
        # list_0_1 = [i for i in range(1, 6)]
        # for url in list_0_1:
            thread = threading.Thread(target=self.send_response, args=[url_make])
            thread.start()
            thread_list_2.append(thread)
            time.sleep(0.1)
            # self.send_request(self.before_url+str(url))
        for thread in thread_list_2:
            thread.join()

        self.fp.close()



if __name__ == '__main__':
    start = time.time()
    spider = Huangye()
    spider.start_work()
    end = time.time()
    print end-start