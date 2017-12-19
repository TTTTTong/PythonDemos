from django.shortcuts import render, render_to_response, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Post, Category
from comments.forms import CommentForm
from django.core.paginator import Paginator
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
# 使用类视图改写视图函数
# ---------------------------------------------------------------------------------------------


class IndexView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    # 类视图中已经写好了分页逻辑，指定了paginate属性后会开启分页功能
    paginate_by = 3

    def get_context_data(self, **kwargs):
        """
        在视图函数中将模板变量传递给模板是通过给 render 函数的 context 参数传递一个字典实现的，
        例如 render(request, 'blog/index.html', context={'post_list': post_list})，
        这里传递了一个 {'post_list': post_list} 字典给模板。
        在类视图中，这个需要传递的模板变量字典是通过 get_context_data 获得的，
        所以我们复写该方法，以便我们能够自己再插入一些我们自定义的模板变量进去。
        """

        # 首先获得父类生成的传递给模板的字典
        context = super().get_context_data(**kwargs)

        # 父类生成的字典中已有 paginator、page_obj、is_paginated 这三个模板变量
        # paginator是Paginator的一个实例
        # page_obj是page的一个实例，即当前页面的分页对象
        paginator = context.get('paginator')
        page_obj = context.get('page_obj')
        is_paginated = context.get('is_paginated')

        pagination_data = self.pagination_data(paginator, page_obj, is_paginated)
        context.update(pagination_data)

        return context

    def pagination_data(self, paginator, page_obj, is_paginated):
        """
        先来分析一下导航条的组成部分，可以看到整个分页导航条其实可以分成 七个部分：
        1.第 1 页页码，这一页需要始终显示。
        2.第 1 页页码后面的省略号部分。但要注意如果第 1 页的页码号后面紧跟着页码号 2，那么省略号就不应该显示。
        3.当前页码的左边部分，比如这里的 3-6。
        4.当前页码，比如这里的 7。
        5.当前页码的右边部分，比如这里的 8-11。
        6.最后一页页码前面的省略号部分。但要注意如果最后一页的页码号前面跟着的页码号是连续的，那么省略号就不应该显示。
        7.最后一页的页码号。
        因此我们的思路是，在视图里将以上七步中所需要的数据生成(当前页码不用计算)，然后传递给模板并在模板中渲染显示即可。
        """
        if not is_paginated:
            return {}

        # 当前页左右的号码
        left = []
        right = []

        # 第一页后面是否需要显示省略号
        left_has_more = False
        # 最后一页前面是否需要显示省略号
        right_has_more =False

        # 是否需要显示第一页和最后一页
        first = False
        last = False

        page_number = page_obj.number  # 当前页
        total_pages = paginator.num_pages  # 总页数
        page_range = paginator.page_range  # 整个分页页码列表(从 1 开始)

        if page_number == 1:
            right = page_range[page_number:page_number + 2]

            if right[-1] < total_pages:
                last = True
            if right[-1] < total_pages - 1:
                right_has_more = True

        elif page_number == total_pages:
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number-1]

            if left[0] > 1:
                first = True
            if left[0] > 2:
                left_has_more = True

        else:
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number-1]
            right = page_range[page_number:page_number + 2]

            if right[-1] < total_pages:
                last = True
            if right[-1] < total_pages - 1:
                right_has_more = True

            if left[0] > 1:
                first = True
            if left[0] > 2:
                left_has_more = True
        data = {
            'first': first,
            'left_has_more': left_has_more,
            'left': left,
            'right': right,
            'right_has_more': right_has_more,
            'last': last,
        }

        return data


class CategoriesView(IndexView):
    def get_queryset(self):
        category = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super().get_queryset().filter(category=category)


class ArchivesView(IndexView):
    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        return super().get_queryset().filter(create_time__year=year,
                                                               create_time__month=month)


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'  # 此处小写

    def get(self, request, *args, **kwargs):
        # 重写get方法是为了在此处将post的阅读量+1
        # get方法返回HttpResponse实例，因为只有调用get之后才有self.object实例即Post对象
        response = super().get(self, request, *args, **kwargs)
        self.object.increase_views()

        # 视图函数必须返回的HttpResponse对象
        return response

    def get_object(self, queryset=None):
        # 重写此方法是为了对post的body值进行渲染
        post = super().get_object(queryset=None)
        post.body = markdown.markdown(post.body, extensions=[
                                        'markdown.extensions.extra',
                                        'markdown.extensions.codehilite',
                                        'markdown.extensions.toc',
                                        ])

        return post

    def get_context_data(self, **kwargs):
        # 重写此方法是为了把评论表单、评论列表传递给模板
        context = super().get_context_data(**kwargs)
        form = CommentForm()
        comment_list = self.object.comment_set.all()

        context.update({
            'form': form,
            'comment_list': comment_list
        })

        return context
