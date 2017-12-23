from django.shortcuts import render, redirect, render_to_response
from django.views.decorators.csrf import csrf_exempt
from .forms import RegisteForm
# Create your views here.


@csrf_exempt
def register(request):
    if request.method == 'POST':
        form = RegisteForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('/')
    else:
        form = RegisteForm()

    return render_to_response('myauth/register.html', context={'form': form})


def index(request):
    return render(request, 'blog/index.html')
