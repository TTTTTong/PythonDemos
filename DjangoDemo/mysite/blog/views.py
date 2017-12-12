from django.shortcuts import render, render_to_response, get_object_or_404
from .models import Post, Category
import markdown
import pygments

# Create your views here.


def index(request):
    title = 'the index'
    welcome = 'welcome'
    post_list = Post.objects.all().order_by('-create_time')
    return render_to_response('blog/index.html', locals())


def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.body = markdown.markdown(post.body, extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc'
    ])
    return render_to_response('blog/detail.html', locals())


def archives(request, year, month):
    # 由于mysql的时区设置，要在setting.py中把USE_TZ改为False
    post_list = Post.objects.filter(create_time__year=year, create_time__month=month).order_by('-create_time')
    return render_to_response('blog/index.html', locals())


def categories(request, pk):
    category = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=category)
    return render_to_response('blog/index.html', locals())
