# -*- coding:utf-8 -*-\
import re
import json
import requests
import urllib
import sys

reload(sys)
sys.setdefaultencoding("utf-8")


# 根据输入的车次与时间，打印出该车从起点到中途每一个站的时间，
# 以及剩余车票数量情况
# 使用去哪网
# 运行环境：python2、linux


class Spider(object):
    def __init__(self, start, end, date):
        self.url = "https://train.qunar.com/dict/open/s2s.do?callback=jQuery17206427667721897028_1517316526987&{0}&{1}&{2}&type=normal&user=neibu&source=site&start=1&num=500&sort=3&_=1517316527616"
        self.headers = {
            'accept': 'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.8',
            'cache-control': 'max-age=0',
            'cookie': 'QN1=dXrgjFpwX0IAxK99Cwc0Ag==; csrfToken=8nYGSSLP9yegSVsYqSkC14HLB5RiBnWT; QN48=tc_5d1fa0352ec83997_16146f44192_c6bf; QN269=B909D95305B511E8AA44FA163E9BF76E; QunarGlobal=10.86.213.129_-18efdd1e_16146ee5e1e_-64cc|1517313869273; QN99=8475; QN300=organic; QN621=1490067914133%3DDEFAULT; QN205=partner; QN277=partner; QN601=0336d8c55464e794babe0c580dc394ae; QN267=1517316313113_db00479692dd60b4; _i=RBTje9LUdxbVNsvT6I89qDAJgeRx; _vi=n8C8rzP2p2OAy9KxBhyiyPawxVJTjRn4GXwi8g4pQtrtZdv8EqQSUnpjh21hawwS8bgNPbFYDZpw82Cy_LaIYuiK9sK_RGSKf3nagnBrItx_Gu7Mi2a9ndj58iaQ5inlh0gmQS8PSzLxZAc0ERqa_dmlgEU-xTov7xy4b6BZPs20; QN268=1517316313113_db00479692dd60b4|1517316526826_9ef3815d158e3998',
            'referer': 'https://train.qunar.com/stationToStation.htm?fromStation=%E5%8C%97%E4%BA%AC&toStation=%E4%B8%8A%E6%B5%B7&date=2018-02-20',
            'x-requested-with': 'XMLHttpRequest',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
        }
        self.start = {'dptStation': start}
        self.end = {'arrStation': end}
        self.date = {'date': date}

    def send_request(self):
        # 请求方法
        start = urllib.urlencode(self.start)
        end = urllib.urlencode(self.end)
        date = urllib.urlencode(self.date)
        response = requests.get(self.url.format(start, end, date))
        return response.content

    def make_html(self, html):
        # 处理response方法
        # print "-1-"*20

        pattern = re.compile(r'\{.*\}')
        text = pattern.search(html)
        # print "-2-" * 20

        text = json.loads(text.group())
        text_list = text['data']['s2sBeanList']
        for i in text_list:
            print "车次：" + i['trainNo']
            print "发车时间：" + i['dptTime']
            print "到达时间：" + i['arrTime']
            print "剩余车票：" + str(i['extraBeanMap']['tickets'])
            print "--" * 20

    def start_work(self):
        html = self.send_request()
        self.make_html(html)


if __name__ == '__main__':
    start = raw_input("请输入首站:")
    end = raw_input("请输入尾站:")
    date = raw_input("请输入日期(格式2000-11-11):")
    spider = Spider(start, end, date)
    spider.start_work()
