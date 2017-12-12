from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.template import RequestContext
from blog.models import Post
from django.views.decorators.csrf import csrf_exempt

from .forms import CommentForm


# Create your views here.
@csrf_exempt
def post_comment(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)

    if request.method == 'POST':
        form = CommentForm(request.POST)

        # Django检查表单是否符合要求
        if form.is_valid():
            # 利用表单数据生成comment实例，此时不保存到数据库
            comment = form.save(commit=False)

            # 将post实例与comment关联后再保存
            comment.post = post
            comment.save()

            # redirect接收到模型实例后会调用模型的get_absolute_url方法，然后重定向到此方法返回的URL
            return redirect(post)
        else:
            comment_list = Post.comment_set.all()
            context = {
                'post': post,
                'form': form,
                'comment_list': comment_list
            }

            return render_to_response('blog/detail.html', context, context_instance=RequestContext(request))

    return redirect(post)
