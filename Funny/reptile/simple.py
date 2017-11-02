import requests
from bs4 import BeautifulSoup

url = 'http://bj.xiaozhu.com/'
page = requests.get(url)
soup = BeautifulSoup(page.text, 'lxml')
selects = ['#page_list > ul > li:nth-of-type({}) > div.result_btm_con.lodgeunitname > '
           'div > a > span'.format(str(i)) for i in range(1, 25)]
for selector in selects:
    re = soup.select(selector)
    print(re[0])


