import requests
import time
import xlwt
from bs4 import BeautifulSoup

first_url = 'https://movie.douban.com/top250'
header ={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                  ' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36'
}
result_dict = {}


def get_rst(url):
    page = requests.get(url, headers=header)
    soup = BeautifulSoup(page.text, 'lxml')
    for i in soup.select('div.hd'):
        desc = i.select('span.inq')  # js加载，暂时未获取
        movie_name = i.select('span.title')[0].text
        if len(i.select('span.title')) == 2:
            movie_name += i.select('span.title')[1].text
        result_dict[movie_name] = desc

    # time.sleep(1)
    if soup.select('span.next > a'):
        next_href = soup.select('span.next > a')[0].get('href')
        get_rst(first_url+next_href)


def to_xls(result_list):
    work = xlwt.Workbook(encoding='utf-8')
    sheet = work.add_sheet('douban_top', cell_overwrite_ok=True)
    sheet.col(0).width = 256*70
    sheet.write(0, 0, '名称')
    sheet.write(0, 1, '评分')
    index = 1
    for name, desc in result_dict.items():
        sheet.write(index, 0, name)
        sheet.write(index, 1, desc)
        index += 1
    work.save('douban_top.xls')


if __name__ == '__main__':
    get_rst(first_url)
    to_xls(result_dict)