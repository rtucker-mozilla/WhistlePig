from django.contrib import admin
from models import StatusUpdate, StatusUpdateComment, Severity, Service, ServiceOutage, Status
from models import SourceEmailAddress, DestinationEmailAddress, OutageNotificationTemplate, TimeZone, Site
class StatusUpdateCommentAdminInline(admin.TabularInline):
    model = StatusUpdateComment


class ServiceOutageAdminInline(admin.TabularInline):
    model = ServiceOutage

class StatusUpdateAdmin(admin.ModelAdmin):
    inlines = (
        ServiceOutageAdminInline,
        StatusUpdateCommentAdminInline,
    )
    class Media:
        js = (
                '/static/whistlepig/js/jquery-1.7.1.min.js',
                '/static/whistlepig/js/statusupdate.js',
            )
    
class OutageNotificationAdmin(admin.ModelAdmin):
    class Media:
        css = {
            'all': ('/static/whistlepig/css/outagenotification.css',)
        }

admin.site.register(StatusUpdate, StatusUpdateAdmin)
admin.site.register(Severity)
admin.site.register(Service)
admin.site.register(Status)
admin.site.register(ServiceOutage)
admin.site.register(SourceEmailAddress)
admin.site.register(DestinationEmailAddress)
admin.site.register(OutageNotificationTemplate, OutageNotificationAdmin)
admin.site.register(TimeZone)
admin.site.register(Site)
admin.site.register(StatusUpdateComment)
