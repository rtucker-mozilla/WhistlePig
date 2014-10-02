from django.contrib.syndication.views import Feed
from models import StatusUpdate
from .feed_views import Feed
class LatestUpdatesFeed(Feed):
    title = "Latest Mozilla Notifications"
    link = "/rss/"
    description = "Updates on notifications and outages at Mozilla"

    def items(self):
        if self.is_anonymous:
            return StatusUpdate.objects.filter(is_private=False).order_by('-posted_on')[:5]
        else:
            return StatusUpdate.objects.order_by('-posted_on')[:5]

    def item_title(self, item):
        if self.is_anonymous and item.is_private:
            return ''
        else:
            return item.summary

    def item_description(self, item):
        if self.is_anonymous and item.is_private:
            return ''
        else:
            return item.description

