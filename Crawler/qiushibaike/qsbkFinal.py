import re
import urllib.request


class QSBK:
    def __init__(self):
        self.pageIndex = 1
        self.user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 ' \
                          '(KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
        self.headers = {'User-Agent': self.user_agent}
        # 每一个元素是每一页的段子们
        self.story = []
        # 程序是否继续运行
        self.enable = False

    def getPage(self, pageIndex):
        # 给定索引返回某一页内容
        try:
            url = 'http://www.qiushibaike.com/hot/page/' + str(pageIndex)
            request = urllib.request.Request(url, headers=self.headers)
            response = urllib.request.urlopen(request)
            content = response.read().decode()

            return content
        except urllib.error.HTTPError as e:
            if hasattr(e, 'reason'):
                print('连接糗事百科失败，原因：', e.reason)
                return None

    def getPageItem(self, pageIndex):
        content = self.getPage(pageIndex)
        if not content:
            print('获取页面失败')

        # pattern = re.compile('<div.*?author">.*?<a.*?<img.*?>(.*?)</a>.*?<div.*?' +
        #                 'content">(.*?)<!--(.*?)-->.*?</div>(.*?)<div class="stats.*?class="number">(.*?)</i>', re.S)
        pattern = re.compile('h2>(.*?)</h2.*?content">.*?<span>(.*?)</span.*?number">(.*?)</.*?number">(.*?)</',
                             re.S)

        items = re.findall(pattern, content)
        # 存储每页的段子
        pageStore = []

        for item in items:
            replaceBR = re.compile('<br/>')
            text = re.sub(replaceBR, '\n', item[1])
            pageStore.append([item[0].strip(), text.strip(), item[2].strip(), item[3].strip()])

        return pageStore

    def loadPage(self):
        # 如果当前为阅读的页数小于一页，则加载新的一页
        if self.enable is True:
            if len(self.story) < 2:
                pageStore = self.getPageItem(self.pageIndex)
                if pageStore:
                    self.story.append(pageStore)
                    self.pageIndex += 1

    # 调用该方法，每次回车打印一个新段子
    def getStory(self, pageStories, page):
        for story in pageStories:
            userinput = input()
            # 每次回车后判断是否要加载新页面
            self.loadPage()

            if userinput == 'Q':
                self.enable = False
                return
            print('第%d页，作者：%s，%s赞，%s评论\t，正文:%s' % (page, story[0], story[2], story[3], story[1]))

    def start(self):
        print('正在读取糗事百科，按回车键继续，Q退出>>>>>')
        self.enable = True
        self.loadPage()
        # 记录观看页数
        nowPage = 0
        while self.enable:
            if len(self.story) > 0:
                pageStories = self.story[0]
                nowPage += 1
                del self.story[0]
                self.getStory(pageStories, nowPage)


if __name__ == '__main__':
    qsbk = QSBK()
    qsbk.start()