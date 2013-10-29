import datetime
import django_cal
from django_cal.views import Events
import dateutil.rrule as rrule
import whistlepig.whistlepig.models as models
from django.conf import settings
import pytz

class iCalEntriesFeed(Events):

    def items(self):
        return models.StatusUpdate.objects.all()

    def cal_name(self):
        return "Mozilla Status Updates"

    def cal_desc(self):
        return "Mozilla Status Updates"

    def item_summary(self, item):
        return item.summary

    def get_time_as_utc(self, input_time, item):
        utc_tz = pytz.timezone('UTC')
        pacific_tz = pytz.timezone('America/Los_Angeles')
        tmp = datetime.datetime(
                input_time.year,
                input_time.month,
                input_time.day,
                input_time.hour,
                input_time.minute,
                input_time.second)
        if item.timezone.name != u'UTC':
            tmp = pacific_tz.localize(datetime.datetime(
                    input_time.year,
                    input_time.month,
                    input_time.day,
                    input_time.hour,
                    input_time.minute,
                    input_time.second))
        else:
            tmp = datetime.datetime(
                    input_time.year,
                    input_time.month,
                    input_time.day,
                    input_time.hour,
                    input_time.minute,
                    input_time.second)
        return tmp.astimezone(utc_tz)

    def item_start(self, item):
        return self.get_time_as_utc(item.start_time, item)

    def item_end(self, item):
        if item.end_time:
            return self.get_time_as_utc(item.end_time, item)
        else:
            return self.get_time_as_utc(item.start_time, item)

    def item_categories(self, item):
        return [i.service.name for i in item.serviceoutage_set.all()]

    def item_url(self, item):
        return "%s/detail/%s/" % (settings.SITE_URL, item.id)

    def __init__(self, *args, **kwargs):
        super(iCalEntriesFeed, self).__init__(*args, **kwargs)
