from django.db import models

class StatusUpdate(models.Model):
    summary = models.CharField(max_length=255, blank=False)
    posted_by = models.CharField(max_length=255, blank=False)
    admin_assigned = models.CharField(max_length=255, blank=False)
    bugzilla_id = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=False)
    created_on = models.DateTimeField(auto_now_add=True)
    posted_on = models.DateTimeField(auto_now_add=True)
    severity = models.ForeignKey('Severity')
    from_bugzilla = models.BooleanField()

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


