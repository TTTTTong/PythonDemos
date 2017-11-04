import requests
import xlwt
from bs4 import BeautifulSoup
"""
爬取小猪网首页上24个房源的信息
"""


# 所有房源的页面
def all_src():
    result = {}
    url = 'http://bj.xiaozhu.com/'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'lxml')
    selects = ['#page_list > ul > li:nth-of-type({}) > a'.format(str(i)) for i in range(1, 25)]

    for k, v in enumerate(selects):
        result[k] = soup.select(v)[0].get('href')
    get_info(result)


def get_info(result):
    for k, v in result.items():
        # time.sleep(1)
        page = requests.get(v)
        soup = BeautifulSoup(page.text, 'lxml')
        rdict = {}

        # name = soup.find_all('title')[0].get_text()
        rdict['name'] = soup.select('div.pho_info > h4')[0].get_text().strip()
        rdict['addr'] = soup.select('div.pho_info > p > span.pr5')[0].get_text().strip()
        rdict['price'] = soup.select('#pricePart > div.day_l > span')[0].get_text()
        rdict['person'] = soup.select('#floatRightBox > div.js_box.clearfix > div.w_240 > h6 > a')[0].get_text()
        rdict['size'] = soup.select('#introduce > li.border_none > p')[0].get_text().split('                         ')[0]
        rdict['type'] = soup.select('#introduce > li.border_none > p')[0].get_text().split('                         ')[1]

        to_xls(rdict, k)


def to_xls(rdict, k):
    k += 1
    sheet.write(k, 0, rdict['name'])
    sheet.write(k, 1, rdict['addr'])
    sheet.write(k, 2, rdict['size'])
    sheet.write(k, 3, rdict['type'])
    sheet.write(k, 4, rdict['price'])
    sheet.write(k, 5, rdict['person'])

    workbook.save('xiaozhu_result.xls')


if __name__ == '__main__':
    workbook = xlwt.Workbook(encoding='utf-8')
    sheet = workbook.add_sheet('xiaozhu_result', cell_overwrite_ok=True)
    # 设置内容在单元格中居中
    alignment = xlwt.Alignment()
    alignment.horz = xlwt.Alignment.HORZ_CENTER
    alignment.vert = xlwt.Alignment.VERT_CENTER
    style = xlwt.XFStyle()
    style.alignment = alignment
    # 设置每列单元格的宽度
    sheet.col(0).width = 256*50
    sheet.col(1).width = 256*50
    sheet.col(2).width = 256*20
    sheet.col(3).width = 256*30
    sheet.col(5).width = 256*30

    sheet.write(0, 0, '名称', style=style)
    sheet.write(0, 1, '地址', style=style)
    sheet.write(0, 2, '面积', style=style)
    sheet.write(0, 3, '户型', style=style)
    sheet.write(0, 4, '价格', style=style)
    sheet.write(0, 5, '联系人', style=style)
    all_src()
