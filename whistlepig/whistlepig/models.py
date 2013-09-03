from django.db import models

class StatusUpdate(models.Model):
    summary = models.CharField(max_length=255, blank=False)
    posted_by = models.CharField(max_length=255, blank=False)
    duration_minutes = models.IntegerField(null = True, blank=True)
    admin_assigned = models.CharField(max_length=255, blank=False)
    bugzilla_id = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=False)
    created_on = models.DateTimeField(auto_now_add=True)
    start_time = models.DateTimeField(null=False, blank=False)
    posted_on = models.DateTimeField(auto_now_add=True)
    severity = models.ForeignKey('Severity')
    status = models.ForeignKey('Status')
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

    def __unicode__(self):
        return self.summary
    
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

class Status(models.Model):
    name = models.CharField(max_length=255, blank=False)

    def __unicode__(self):
        return self.name
class ServiceOutage(models.Model):
    status_update = models.ForeignKey('StatusUpdate')
    service = models.ForeignKey('Service')

    def __unicode__(self):
        return "%s - %s" % (self.status_update, self.service)

class Service(models.Model):
    name = models.CharField(max_length=255, blank=False)

    def __unicode__(self):
        return self.name

class SourceEmailAddress(models.Model):
    name = models.CharField(max_length=255, blank=False)
    short_description = models.CharField(max_length=255, blank=False)

    def __unicode__(self):
        return self.name

class DestinationEmailAddress(models.Model):
    name = models.CharField(max_length=255, blank=False)

    def __unicode__(self):
        return self.name

class OutageNotificationTemplate(models.Model):
    outage_notification_template = models.TextField(blank=False)
