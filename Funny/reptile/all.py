from pprint import pprint
import requests
import time
from bs4 import BeautifulSoup
"""
爬去小猪网首页上25个房源的信息
"""


# 所有房源的页面
def all_src():
    result = []
    url = 'http://bj.xiaozhu.com/'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'lxml')
    selects = ['#page_list > ul > li:nth-of-type({}) > a'.format(str(i)) for i in range(1, 25)]

    for sl in selects:
        result.append(soup.select(sl)[0].get('href'))

    get_info(result)


def get_info(result):
    for i in result:
        time.sleep(1)
        page = requests.get(i)
        soup = BeautifulSoup(page.text, 'lxml')
        rdict = {}

        # name = soup.find_all('title')[0].get_text()
        rdict['name'] = soup.select('div.pho_info > h4')[0].get_text().strip()
        rdict['addr'] = soup.select('div.pho_info > p > span.pr5')[0].get_text().strip()
        rdict['price'] = soup.select('#pricePart > div.day_l > span')[0].get_text()
        rdict['person'] = soup.select('#floatRightBox > div.js_box.clearfix > div.w_240 > h6 > a')[0].get_text()
        rdict['size'] = soup.select('#introduce > li.border_none > p')[0].get_text()

        pprint(rdict)


if __name__ == '__main__':
    all_src()