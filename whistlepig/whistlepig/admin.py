from django.contrib import admin
from models import StatusUpdate, Severity, Service, ServiceOutage, Status
from models import SourceEmailAddress, DestinationEmailAddress, OutageNotificationTemplate, TimeZone, Site
class ServiceOutageAdminInline(admin.TabularInline):
    model = ServiceOutage

class StatusUpdateAdmin(admin.ModelAdmin):
    inlines = (ServiceOutageAdminInline,)
    class Media:
        js = (
                '/static/whistlepig/js/jquery-1.7.1.min.js',
                '/static/whistlepig/js/statusupdate.js',
                
            )
    

admin.site.register(StatusUpdate, StatusUpdateAdmin)
admin.site.register(Severity)
admin.site.register(Service)
admin.site.register(Status)
admin.site.register(ServiceOutage)
admin.site.register(SourceEmailAddress)
admin.site.register(DestinationEmailAddress)
admin.site.register(OutageNotificationTemplate)
admin.site.register(TimeZone)
admin.site.register(Site)
