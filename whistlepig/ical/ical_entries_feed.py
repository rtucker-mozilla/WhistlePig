import datetime
import django_cal
from django_cal.views import Events
import dateutil.rrule as rrule
import whistlepig.whistlepig.models as models
from django.conf import settings

class iCalEntriesFeed(Events):

    _items = []

    def items(self):
        return self._items

    def cal_name(self):
        return "Mozilla Status Updates"

    def cal_desc(self):
        return "Mozilla Status Updates"

    def item_summary(self, item):
        return item.summary

    def item_start(self, item):
        return item.start_time

    def item_end(self, item):
        if item.end_time:
            return item.end_time
        else:
            return item.start_time

    def item_categories(self, item):
        return [i.service.name for i in item.serviceoutage_set.all()]

    def item_url(self, item):
        return "%s/detail/%s/" % (settings.SITE_URL, item.id)

    def __init__(self, *args, **kwargs):
        self._items = models.StatusUpdate.objects.all()
        super(iCalEntriesFeed, self).__init__(*args, **kwargs)
