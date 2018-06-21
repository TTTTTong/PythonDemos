from django.contrib.syndication.views import Feed
from .models import Post


class AllPostRssFeed(Feed):
    # Rss阅读器上的标题
    title = 'Django Blog Demo'

    # 通过Rss阅读器跳转到网站的地址(不知道有啥用，删了也能跳转)
    link = '/'

    # Rss阅读器上显示的描述信息
    description = 'Django Rss Test'

    # 需要显示的内容条目
    def items(self):
        return Post.objects.all()

    # 显示条目的标题
    def item_title(self, item):
        return '[%s] %s' % (item.category, item.title)

    def item_description(self, item):
        return item.body
