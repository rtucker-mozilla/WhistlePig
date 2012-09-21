from django.conf.urls.defaults import patterns, url
from django.views.generic.simple import redirect_to
from django.conf import settings
from feeds import LatestUpdatesFeed

from . import views

urlpatterns = patterns('',
    url(r'^$', views.home, name='whistlepig.home'),
    url(r'^detail/(?P<id>\d+)[/]$', views.detail, name='article-detail'),
    url(r'^rss[/]$', LatestUpdatesFeed(), name='rss'),
)
