from django.db import models

class StatusUpdate(models.Model):
    summary = models.CharField(max_length=255, blank=False)
    posted_by = models.CharField(max_length=255, blank=False)
    duration_minutes = models.IntegerField(null = True, blank=True)
    admin_assigned = models.CharField(max_length=255, blank=False)
    bugzilla_id = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=False)
    created_on = models.DateTimeField(auto_now_add=True)
    start_time = models.DateTimeField(null=True, blank=True)
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


