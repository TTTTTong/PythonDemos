from django.db.models import Count

from ..models import Post, Category, Tag
from django import template

register = template.Library()


@register.simple_tag
def get_recent_posts(num=5):
    return Post.objects.all().order_by('-create_time')[:num]


@register.simple_tag
def archives():
    # 按时间归档，精确到月
    return Post.objects.dates('create_time', 'month', order='DESC')


@register.simple_tag
def get_categories():
    # annotate()方法类似于all(), 但是会做一些额外的事情
    # 在这里让它通过外键计算 post 的数量然后存放在 category 的 num_posts 属性中
    # gt == greater than(gte == greater than or equal )
    return Category.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)
    # .all()的写法可以在html中直接使用 category.post_set.all 来计数，但是会多次查询数据库
    # return Category.objects.all()


@register.simple_tag
def get_tags():
    return Tag.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)
