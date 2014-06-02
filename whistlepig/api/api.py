from tastypie.resources import ModelResource
from whistlepig.whistlepig.models import StatusUpdate, Severity, Service, ServiceOutage, Status
from tastypie.serializers import Serializer
from tastypie.authorization import Authorization
from tastypie.authorization import DjangoAuthorization
from django.core.exceptions import ValidationError
from tastypie.authentication import Authentication, BasicAuthentication
from django.core.serializers import json as djson
from tastypie.authorization import DjangoAuthorization
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
import json
from tastypie import fields

class PrettyJSONSerializer(Serializer):
    json_indent = 2

    def to_json(self, data, options=None):
        options = options or {}
        data = self.to_simple(data, options)
        return json.dumps(data, cls=djson.DjangoJSONEncoder,
                sort_keys=True, ensure_ascii=False, indent=self.json_indent)

class WhistlepigAuthentication(BasicAuthentication):

    def is_authenticated(self, request, **kwargs):
        if request.method == 'GET':
            return True
        return super( WhistlepigAuthentication, self ).is_authenticated( request, **kwargs )

class WhistlepigAuthorization(DjangoAuthorization):

    def is_authorized(self, request, object=None):
        if request.method == 'GET':
            return True
        else:
            return super( WhistlepigAuthorization, self ).is_authorized( request, object )

class CustomAPIResource(ModelResource):
    def __init__(self, *args, **kwargs):
        super(CustomAPIResource, self).__init__(*args, **kwargs)

    def determine_format(self, request):
        format = request.GET.get('format')
        if format:
            return super(CustomAPIResource, self).determine_format(request)
        else:
            return "application/json"

    class Meta:
        serializer = PrettyJSONSerializer()
        authorization = WhistlepigAuthorization()
        authentication = WhistlepigAuthentication()
        allowed_methods = ['get', 'post', 'put', 'delete', 'patch', 'PATCH']


class StatusUpdateResource(ModelResource):
    severity = fields.ForeignKey('whistlepig.api.api.SeverityResource', 'severity', null=True, full=True)
    status = fields.ForeignKey('whistlepig.api.api.StatusResource', 'status', null=True, full=True)
    service_outages = fields.ToManyField('whistlepig.api.api.ServiceOutageResource', 'serviceoutage', null=True)
    service_outages_set = fields.ToManyField('whistlepig.api.api.ServiceOutageResource', 'serviceoutage_set', null=True)
    class Meta(CustomAPIResource.Meta):
        filtering = {
            'summary': ALL,
            'admin_assigned': ALL,
            'description': ALL,
            'bugzilla_id': ALL,
            'posted_by': ALL,
            'posted_on': ALL,
            'service_outages': ALL_WITH_RELATIONS,
            'severity': ALL_WITH_RELATIONS,
            'status': ALL_WITH_RELATIONS,
        }
        queryset = StatusUpdate.objects.filter(is_private = False)

class ServiceOutageResource(ModelResource):
    status_update = fields.ForeignKey('whistlepig.api.api.StatusUpdateResource', 'statusupdate', null=True, full=True)
    service = fields.ForeignKey('whistlepig.api.api.ServiceResource', 'service', null=True, full=True)
    class Meta(CustomAPIResource.Meta):
        filtering = {
            'status_update': ALL_WITH_RELATIONS,
            'service': ALL_WITH_RELATIONS,

        }
        resource_name = 'serviceoutage'
        queryset = ServiceOutage.objects.all()

class StatusResource(ModelResource):
    class Meta(CustomAPIResource.Meta):
        filtering = {
            'name': ALL,
        }
        queryset = Status.objects.all()


class SeverityResource(ModelResource):
    class Meta(CustomAPIResource.Meta):
        filtering = {
            'name': ALL,
        }
        queryset = Severity.objects.all()

class ServiceResource(ModelResource):
    class Meta(CustomAPIResource.Meta):
        filtering = {
            'name': ALL,
        }
        queryset = Service.objects.all()
