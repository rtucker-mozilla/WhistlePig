from django.contrib.syndication.views import Feed
from models import StatusUpdate
class LatestUpdatesFeed(Feed):
    title = "Latest Mozilla Notifications"
    link = "/rss/"
    description = "Updates on notifications and outages at Mozilla"

    def items(self):
        return StatusUpdate.objects.order_by('-posted_on')[:5]

    def item_title(self, item):
        return item.summary

    def item_description(self, item):
        return item.description

