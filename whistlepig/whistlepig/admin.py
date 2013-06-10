from django.contrib import admin
from models import StatusUpdate, Severity, Service, ServiceOutage, Status
class ServiceOutageAdminInline(admin.TabularInline):
    model = ServiceOutage

class StatusUpdateAdmin(admin.ModelAdmin):
    inlines = (ServiceOutageAdminInline,)

admin.site.register(StatusUpdate, StatusUpdateAdmin)
admin.site.register(Severity)
admin.site.register(Service)
admin.site.register(Status)
admin.site.register(ServiceOutage)
