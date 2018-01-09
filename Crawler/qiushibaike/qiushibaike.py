import re
import urllib.request
from pprint import pprint

page = 1
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) ' \
             'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
headers = {'User-Agent': user_agent}

url = 'http://www.qiushibaike.com/hot/page/' + str(page)

try:
    request = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(request)
    content = response.read().decode('utf-8')
    # pattern = re.compile('<div.*?author">.*?<a.*?<img.*?>(.*?)</a>.*?<div.*?' +
    #                      'content">(.*?)<!--(.*?)-->.*?</div>(.*?)<div class="stats.*?class="number">(.*?)</i>', re.S)
    pattern = re.compile('h2>(.*?)</h2.*?content">.*?<span>(.*?)</span.*?number">(.*?)</.*?number">(.*?)</', re.S)

    items = re.findall(pattern, content)

    for item in items:
        # haveImg = re.search('img', item[3])
        # if not haveImg:
        print('作者：', item[0].strip(), item[1].strip(), item[2].strip(), '点赞', item[3].strip(), '评论')


except urllib.error.HTTPError as e:
    if hasattr(e, 'code'):
        print(e.code)
    if hasattr(e, 'reason'):
        print(e.reason)

