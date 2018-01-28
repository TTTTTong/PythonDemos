import re
import requests
from bs4 import BeautifulSoup


class Spider:
    def __init__(self):
        self.url = 'https://mm.taobao.com/json/request_top_list.htm?page='
        self.names = []
        self.ages = []
        self.addrs = []
        self.icons = []
        self.detailURLs = []

    def getList(self, pageIndex):
        response = requests.get(self.url + str(pageIndex))
        soup = BeautifulSoup(response.text, 'lxml')

        for result in soup.select(' div.pic-word > p.top'):
            result = result.text.split()
            self.names.append(result[0])
            self.ages.append(result[1])
            self.addrs.append(result[2])

        for result in soup.select('div.personal-info > div.pic-word > div'):
            self.detailURLs.append('https:' + result.select('a')[0].get('href'))
            self.icons.append('https:' + result.select('a > img')[0].get('src'))

        # print(list(zip(self.detailURLs, self.names, self.addrs, self.ages, self.icons)))

        # pattern = re.compile('<div class="list-item".*?pic-word.*?<a href="(.*?)".*?<img src="(.*?)".*?<a class="lady-name.*?>(.*?)</a>.*?<strong>(.*?)</strong>.*?<span>(.*?)</span>',re.S)
        # items = re.findall(pattern,response.text)
        # for item in items:
        #     print (item[0],item[1],item[2],item[3],item[4])

    def getImage(self):
        for detailURL in self.detailURLs:
            response = requests.get(detailURL)
            print(response.text)
            soup = BeautifulSoup(response.text, 'lxml')
            allImagePage = soup.select('div.mm-aixiu-content > div > img')
            # print(allImagePage)
            break



new = Spider()
new.getList(1)
new.getImage()
