import re
import urllib.request
from pprint import pprint


# 爬虫类
class BDTB:
    # 初始化传入基本地址和是否只看楼主参数
    def __init__(self, baseURL, seeLz):
        self.baseURL = baseURL
        self.seeLz = '?see_lz=' + str(seeLz)
        self.tool = Tool()

    def getPage(self, pageNum):
        try:
            url = self.baseURL + self.seeLz + '&pn=' + str(pageNum)
            request = urllib.request.Request(url)
            response = urllib.request.urlopen(request)

            return response.read().decode()
        except urllib.error.HTTPError as e:
            if hasattr(e, 'reason'):
                print('连接百度贴吧出错，原因：', e.reason)
                return None

    def getTitle(self):
        page = self.getPage(1)
        pattern = re.compile('class="core_title_txt pull-left text-overflow.*?>(.*?)</h3>', re.S)
        title = re.search(pattern, page)

        if title:
            return title.group(1).strip()
        else:
            return None

    def getCountPage(self):
        # 获取共有多少页回帖
        page = self.getPage(1)
        pattern = re.compile('class="l_reply_num".*?</span>.*?<span.*?>(.*?)</span>', re.S)
        pageNum = re.search(pattern, page)

        if pageNum:
            return pageNum.group(1).strip()
        else:
            return None

    def getContent(self, page):
        '''
        获取每一页的所有楼层的回复
        :param page: 传入页面
        :return: 所有回复的集合list
        '''

        pattern = re.compile('class="d_post_content j_d_post_content.*?>(.*?)</div>')
        result = re.findall(pattern, page)

        index = 1
        for item in result:
            print(self.tool.replace(item))
            print('-----------------------', index, '楼---------------------------------------------------------')
            index += 1


# 处理标签的工具类
class Tool:
    removeImg = re.compile('<img .*?>')
    removeHref = re.compile('<a .*?>|</a>')
    # 替换换行符
    replaceLine = re.compile('<br>')
    # 把其余标签删除
    removeOther = re.compile('<.*?>')

    def replace(self, content):
        content = re.sub(self.removeImg, '', content)
        content = re.sub(self.removeHref, '', content)
        content = re.sub(self.replaceLine, '\n', content)
        content = re.sub(self.removeOther, '', content)

        return content.strip()


if __name__ == '__main__':
    baseURL = 'https://tieba.baidu.com/p/3138733512'
    new = BDTB(baseURL, 1)
    # new.getPage(1)
    new.getContent(new.getPage(1))