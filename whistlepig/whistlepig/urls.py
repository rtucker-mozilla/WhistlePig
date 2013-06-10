from django.conf.urls.defaults import patterns, url
from django.views.generic.simple import redirect_to
from django.conf import settings
from feeds import LatestUpdatesFeed

from . import views

urlpatterns = patterns('',
    url(r'^$', views.home, name='whistlepig.home'),
    url(r'search[/]$', views.search, name='whistlepig.search'),
    url(r'calendar[/]$', views.calendar, name='whistlepig.calendar'),
    url(r'event_feed$', views.event_feed, name='whistlepig.event_feed'),
    url(r'^detail/(?P<id>\d+)[/]$', views.detail, name='article-detail'),
    url(r'^rss[/]$', LatestUpdatesFeed(), name='rss'),
)
