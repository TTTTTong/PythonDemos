from django.shortcuts import render, render_to_response
from django.http import HttpResponse

# Create your views here.
from .models import Post


def index(request):
    title = 'the index'
    welcome = 'welcome'
    post_list = Post.objects.all().order_by('-create_time')
    return render_to_response('blog/index.html', locals())
