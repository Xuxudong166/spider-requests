# -*- coding:utf-8 -*-\
import csv
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import requests
import urllib2
import urllib
from lxml import etree
import json
from Queue import Queue
import threading
import time

class Spider(object):
    """拉勾网爬虫"""
    def __init__(self, city):
        self.url = "https://www.lagou.com/jobs/positionAjax.json?"
        self.url_xq = 'https://www.lagou.com/jobs/'
        self.fromdata = {
            'px': 'default',
            'city': city,
            'needAddtionalResult': 'false',
            'isSchoolJob': '0'
        }

        self.proxy = {"https": "https://101.68.73.54:53281"}

        self.headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Connection': 'keep-alive',
            'Content-Length': '44',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': 'user_trace_token=20171214173555-2eae0f92-e0b2-11e7-9793-525400f775ce; LGUID=20171214173555-2eae1652-e0b2-11e7-9793-525400f775ce; JSESSIONID=ABAAABAAAFCAAEGA6983036DD6BC4BC22A19CB0A7DD1A06; X_HTTP_TOKEN=1dd130608e88a83a9915c76c03dd0ecf; ab_test_random_num=0; SEARCH_ID=94f21f8c23a04c50a8d86af7a8d4d9fd; TG-TRACK-CODE=search_code; index_location_city=%E4%B8%8A%E6%B5%B7; _gid=GA1.2.88707154.1515896926; _ga=GA1.2.1638177916.1513244159; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1515335491,1515896927,1515896934,1515896940; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1515899017; LGSID=20180114102851-a8c3b54d-f8d2-11e7-94f9-525400f775ce; LGRID=20180114110334-82412e69-f8d7-11e7-a2ef-5254005c3644',
            'Host': 'www.lagou.com',
            'Origin': 'https://www.lagou.com',
            'Referer': 'https://www.lagou.com/jobs/list_python%E7%88%AC%E8%99%AB?px=default&city=%E4%B8%8A%E6%B5%B7',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
            'X-Anit-Forge-Code': '0',
            'X-Anit-Forge-Token': 'None',
            'X-Requested-With': 'XMLHttpRequest'
        }
        self.headers2 = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Cookie': 'user_trace_token=20171214173555-2eae0f92-e0b2-11e7-9793-525400f775ce; LGUID=20171214173555-2eae1652-e0b2-11e7-9793-525400f775ce; JSESSIONID=ABAAABAAAFCAAEGA6983036DD6BC4BC22A19CB0A7DD1A06; X_HTTP_TOKEN=1dd130608e88a83a9915c76c03dd0ecf; ab_test_random_num=0; SEARCH_ID=94f21f8c23a04c50a8d86af7a8d4d9fd; TG-TRACK-CODE=search_code; index_location_city=%E4%B8%8A%E6%B5%B7; _gid=GA1.2.88707154.1515896926; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1515335491,1515896927,1515896934,1515896940; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1515901662; _ga=GA1.2.1638177916.1513244159; LGRID=20180114114739-aaa6eaaa-f8dd-11e7-a2f1-5254005c3644',
            'Host': 'www.lagou.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
        }
        self.queue = Queue()

        self.fp = file('lagouspider.csv', "a")
        self.csv_writer = csv.writer(self.fp)
        item = {"公司名": "", "招聘岗位": "", "工资范围": "", "公司地址": "", "公司网站": "", "岗位描述": ""}
        sheet = item.keys()
        self.csv_writer.writerow(sheet)

    def send_request(self, url, data, headers):
        request = requests.post(url, data=data, headers=headers)
        self.make_url(request.content)

    def send_response(self, url):
        request = requests.get(url, headers=self.headers2)
        self.make_html(request.content)
        # return request.content

    def make_url(self, jsons):
        dict_ = json.loads(jsons)
        list_ = dict_['content']['positionResult']['result']
        for i in list_:
            # print i['positionId']

            self.queue.put(self.url_xq+str(i['positionId'])+'.html')

    def make_html(self, html):
        html_obj = etree.HTML(html)
        # 公司名
        company_name = html_obj.xpath("//div[@class='company']/text()")
        # 招收岗位
        job_name = html_obj.xpath("//div[@class='job-name']/span[@class='name']/text()")
        # 工资范围
        money = html_obj.xpath("//span[@class='salary']/text()")
        # 公司地址
        company_adr = html_obj.xpath("//div[@class='work_addr']/a/text()")
        # 公司网站
        company_web = html_obj.xpath("//ul[@class='c_feature']//a/@href")
        # 岗位描述
        job_duty = html_obj.xpath("//dd[@class='job_bt']/div/p/text()")

        item = {}
        item['公司名'] = company_name[0]
        item['招收岗位'] = job_name[0]
        item['工资范围'] = money[0]
        company_adr_result = ""
        for i in company_adr[:3]:
            company_adr_result += i+"/"
        item['公司地址'] = company_adr_result
        item['公司网站'] = company_web[0]
        job_duty_result = ""
        for n in job_duty:
            job_duty_result += n+";"
        item['岗位描述'] = job_duty_result
        data = item.values()
        self.csv_writer.writerow(data)

    def start_work(self):
        list_thread_ = []
        for o in range(1, 10):
            self.data = {
                'first': 'false',
                'pn': str(o),
                'kd': 'python爬虫'
            }
            fromdata = urllib.urlencode(self.fromdata)

            thread1 = threading.Thread(target=self.send_request, args=[self.url+fromdata, self.data, self.headers])

            thread1.start()
            list_thread_.append(thread1)
            time.sleep(0.1)
        for m in list_thread_:
            m.join()

        list_thread = []
        while not self.queue.empty():
            url_xq = self.queue.get()
            thread = threading.Thread(target=self.send_response, args=[url_xq])
            print url_xq
            thread.start()
            list_thread.append(thread)
            time.sleep(0.1)
        for i in list_thread:
            i.join()
            # html = self.send_response(url_xq, self.headers2)
        self.fp.close()

if __name__ == '__main__':
    city = raw_input('请输入城市名：')
    spider = Spider(str(city))
    spider.start_work()
