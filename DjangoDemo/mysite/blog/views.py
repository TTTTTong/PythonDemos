from django.shortcuts import render, render_to_response, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Post, Category
from comments.forms import CommentForm
import markdown
import pygments


# def index(request):
#     title = 'the index'
#     welcome = 'welcome'
#     post_list = Post.objects.all().order_by('-create_time')
#     return render_to_response('blog/index.html', locals())


# def detail(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     post.increase_views()  # 阅读量+1
#     post.body = markdown.markdown(post.body, extensions=[
#         'markdown.extensions.extra',
#         'markdown.extensions.codehilite',
#         'markdown.extensions.toc'
#     ])
#     form = CommentForm()
#     comment_list = post.comment_set.all()
#     return render_to_response('blog/detail.html', locals())


# def archives(request, year, month):
#     # 由于mysql的时区设置，要在setting.py中把USE_TZ改为False
#     post_list = Post.objects.filter(create_time__year=year, create_time__month=month).order_by('-create_time')
#     return render_to_response('blog/index.html', locals())


# def categories(request, pk):
#     category = get_object_or_404(Category, pk=pk)
#     post_list = Post.objects.filter(category=category)
#     return render_to_response('blog/index.html', locals())


# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------
# 使用类视图改写视图函数
class IndexView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'


class CategoriesView(IndexView):
    def get_queryset(self):
        category = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoriesView, self).get_queryset().filter(category=category)


class ArchivesView(IndexView):
    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        return super(ArchivesView, self).get_queryset().filter(create_time__year=year,
                                                               create_time__month=month)


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'  # 此处小写

    def get(self, request, *args, **kwargs):
        # 重写get方法是为了在此处将post的阅读量+1
        # get方法返回HttpResponse实例，因为只有调用get之后才有self.object实例即Post对象
        response = super(PostDetailView, self).get(self, request, *args, **kwargs)
        self.object.increase_views()

        # 视图函数必须返回的HttpResponse对象
        return response

    def get_object(self, queryset=None):
        # 重写此方法是为了对post的body值进行渲染
        post = super(PostDetailView, self).get_object(queryset=None)
        post.body = markdown.markdown(post.body, extensions=[
                                        'markdown.extensions.extra',
                                        'markdown.extensions.codehilite',
                                        'markdown.extensions.toc',
                                        ])

        return post

    def get_context_data(self, **kwargs):
        # 重写此方法是为了把评论表单、评论列表传递给模板
        context = super(PostDetailView, self).get_context_data(**kwargs)
        form = CommentForm()
        comment_list = self.object.comment_set.all()

        context.update({
            'form': form,
            'comment_list': comment_list
        })

        return context
