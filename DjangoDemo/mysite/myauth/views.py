from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from .forms import RegisterForm

# Create your views here.


@csrf_protect
def register(request):
    if request == 'POST':
        # request.POST是一个字典类数据结构，记录用户提交的注册信息
        form = RegisterForm(request.POST)

        if form.is_valid():
                form.save()

        return redirect('/')
    # 非POST请求说明用户访问注册页面，返回注册表单
    else:
        form = RegisterForm()

        return render(request, 'myauth/register.html', locals())