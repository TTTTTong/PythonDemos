from django.conf.urls import url
from . import views
from .feeds import AllPostRssFeed

app_name = 'blog'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^post/(?P<pk>[0-9]+)/$', views.PostDetailView.as_view(), name='detail'),
    url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', views.ArchivesView.as_view(), name='archives'),
    url(r'^categories/(?P<pk>[0-9]+)/$', views.CategoriesView.as_view(), name='categories'),
    url(r'^tags/(?P<pk>[0-9]+)/$', views.TagView.as_view(), name='tags'),
    url(r'^all/rss/$', AllPostRssFeed(), name='rss'),
]
