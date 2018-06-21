from datetime import datetime

from django.shortcuts import render_to_response


def date(request):
    now = datetime.now()
    return render_to_response('date.html', locals())


def search(request):
    return render_to_response('search.html')