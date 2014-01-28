from django.db import models
import re
from django.conf import settings

class StatusUpdate(models.Model):
    summary = models.CharField('Short Summary', max_length=255, blank=False)
    posted_by = models.CharField(max_length=255, blank=False)
    duration_minutes = models.IntegerField(null = True, blank=True)
    admin_assigned = models.CharField(max_length=255, blank=False)
    bugzilla_id = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=False)
    impact_of_work = models.TextField(blank=False)
    created_on = models.DateTimeField(auto_now_add=True)
    start_time = models.DateTimeField(null=False, blank=False)
    end_time = models.DateTimeField(null=True, blank=True)
    posted_on = models.DateTimeField(auto_now_add=True)
    severity = models.ForeignKey('Severity')
    status = models.ForeignKey('Status')
    frontpage = models.BooleanField('Display on Homepage', default = True)
    timezone = models.ForeignKey('TimeZone')
    site = models.ForeignKey('Site', null=True)
    from_bugzilla = models.BooleanField()

    search_fields = (
            'summary',
            'description',
            'bugzilla_id',
            'severity__name',
            'posted_by',
            'admin_assigned',
            'serviceoutage__service__name',
    )

    class Meta:
        verbose_name_plural = 'Status Updates'

    def expand_bug(self, input_val):
        regex = '[B|b]ug (\d+)'
        matches = re.findall(regex, input_val)
        if matches:
            for m in matches:
                input_val = re.sub('[B|b]ug %s' % m, "<a href='https://bugzil.la/%s'>Bug %s</a>" % (m, m), input_val)
        return input_val

    def expand(self, input_val):
        input_val = self.expand_bug(input_val)
        return input_val

    @property
    def impact_of_work_expanded(self):
        return self.expand(self.impact_of_work)

    @property
    def summary_expanded(self):
        return self.expand(self.summary)

    @property
    def description_expanded(self):
        return self.expand(self.description)

    def __unicode__(self):
        return self.summary

    @property
    def event_start_date(self):
        return self.start_time.strftime("%Y-%m-%d")
    
    @property
    def event_start_time(self):
        return self.start_time.strftime("%H:%M")

    @property
    def event_end_date(self):
        return self.end_time.strftime("%Y-%m-%d")
    
    @property
    def event_end_time(self):
        return self.end_time.strftime("%H:%M")
    
    @property
    def services(self):
        return ", ".join([s.service.name for s in self.serviceoutage_set.all()])

    @property
    def bugzilla_links(self):
        ret_string = ''
        bugs = self.bugzilla_id.replace(' ','')
        bugs = bugs.split(',')
        counter = 1
        for bug in bugs:
            ret_string += '<a href="%s%s">%s</a>' % (settings.BUGZILLA_URL, bug, bug)
            if counter < len(bugs):
                ret_string += ', '
            counter += 1
        return ret_string

    @models.permalink
    def get_absolute_url(self):
        return ('article-detail', [self.id])

    def expand_minutes(self):
        input_minutes = self.duration_minutes
        hours = input_minutes / 60
        minutes = input_minutes % 60
        if hours == 1:
            hour_string = 'hour'
        else:
            hour_string = 'hours'

        if minutes == 1:
            minute_string = 'minute'
        else:
            minute_string = 'minutes'

        if hours > 0 and minutes == 0:
            return "%s %s" % (
                    hours,
                    hour_string
                    )

        elif hours == 0 and minutes > 0:
            return "%s %s" % (
                    minutes,
                    minute_string
                    )
        else:                                                                                                             
            return "%s %s %s %s" % (
                    hours,
                    hour_string,
                    minutes,
                    minute_string
                    )

class Severity(models.Model):
    name = models.CharField(max_length=255, blank=False)
    css_class = models.CharField(max_length=255, blank=False)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Severeties'

class Status(models.Model):
    name = models.CharField(max_length=255, blank=False)

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Statuses'


class ServiceOutage(models.Model):
    status_update = models.ForeignKey('StatusUpdate')
    service = models.ForeignKey('Service')

    def __unicode__(self):
        return "%s - %s" % (self.status_update, self.service)

    class Meta:
        verbose_name_plural = 'Service Outages'


class Service(models.Model):
    name = models.CharField(max_length=255, blank=False)

    def __unicode__(self):
        return self.name

class SourceEmailAddress(models.Model):
    name = models.CharField(max_length=255, blank=False)
    short_description = models.CharField(max_length=255, blank=False)

    def __unicode__(self):
        return self.name

class TimeZone(models.Model):
    name = models.CharField(max_length=255, blank=False)

    def __unicode__(self):
        return self.name

class Site(models.Model):
    name = models.CharField(max_length=255, blank=False)

    def __unicode__(self):
        return self.name

class StatusUpdateComment(models.Model):
    author = models.CharField(max_length=255, blank=False)
    comment = models.TextField(blank=False)
    created_on = models.DateTimeField(auto_now_add=True)
    statusupdate = models.ForeignKey('StatusUpdate')

    def __unicode__(self):
        return "%s - %s" % (self.author, self.created_on)

class DestinationEmailAddress(models.Model):
    name = models.CharField(max_length=255, blank=False)

    def __unicode__(self):
        return self.name

class OutageNotificationTemplate(models.Model):
    interpolated_variable_hash = {}
    name = models.CharField(max_length=255, blank=False)
    subject = models.CharField(max_length=255, blank=False)
    outage_notification_template = models.TextField(blank=False)

    def extract_variable_to_interpolate(self, input_line):
        var_re = re.compile('<<([^>><<]*)>>')
        result = var_re.findall(input_line)
        if not result:
            return None
        else:
            rethash = {}
            for r in result:
                rethash['<<%s>>' % r] = r
                self.interpolated_variable_hash['<<%s>>' % r] = r
            return rethash


    def interpolate(self, status_update, template):
        self.status_update = status_update
        for line in template.split():
            self.extract_variable_to_interpolate(line)
        for k in self.interpolated_variable_hash.iterkeys():
            try:
                template = template.replace(k, str(getattr(status_update, self.interpolated_variable_hash[k])))
            except (AttributeError):
                pass
        return template

    def interpolate_subject(self, status_update = None, template = None):
        if not template:
            template = self.subject
        return self.interpolate(status_update, template)

    def interpolate_template(self, status_update = None, template = None):
        self.status_update = status_update
        if not template:
            template = self.outage_notification_template
        return self.interpolate(status_update, template)

    def __init__(self, *args, **kwargs):
        self.interpolated_variable_hash = {}
        super(OutageNotificationTemplate, self).__init__(*args, **kwargs)

    def __unicode__(self):
        return self.name
