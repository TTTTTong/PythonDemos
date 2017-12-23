from django.conf.urls import url
from . import views


app_name = 'myauth'
urlpatterns = [
    url(r'', views.index, name='index'),
    url(r'^myauth/register/$', views.register, name='register'),
]