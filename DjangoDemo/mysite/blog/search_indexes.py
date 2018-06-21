from haystack import indexes
from .models import Post


class PostIndex(indexes.SearchIndex, indexes.Indexable):
    # 每个索引里面必须有且只能有一个字段为 document=True
    # 这代表 django haystack 和搜索引擎将使用此字段的内容作为索引进行检索(primary field)
    # use_template表明使用templates/search/indexes/blog/post_text.txt.txt路径下的数据模板建立搜索引擎的文件
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Post

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
