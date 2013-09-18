from django.test import Client
from test_utils import TestCase, RequestFactory, setup_test_environment
from django.core.urlresolvers import reverse
import json


class ApiTest(TestCase):
    fixtures = ['whistlepig']

    def setUp(self):
        self.client = Client()
        self.rf = RequestFactory()

    def test1_get_api_endpoint(self):
        response = self.client.get('/api/v1/statusupdate', follow=True)
        self.assertEqual(response.status_code, 200)

    def test2_get_api_statusupdate(self):
        response = self.client.get('/api/v1/statusupdate/11/', follow=True)
        response_obj = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_obj['from_bugzilla'],False)
        self.assertEqual(response_obj['bugzilla_id'],'')
        self.assertEqual(response_obj['description'],'This is a live test from the database')
        self.assertEqual(response_obj['severity']['id'],2)
        self.assertEqual(response_obj['severity']['name'],'No Downtime')
        self.assertEqual(response_obj['posted_by'],'rtucker')
        self.assertEqual(response_obj['admin_assigned'],'rtucker')

    def test3_get_api_statusupdate_with_service_outages(self):
        response = self.client.get('/api/v1/statusupdate/6/', follow=True)
        response_obj = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_obj['from_bugzilla'],False)
        self.assertEqual(response_obj['bugzilla_id'],'123456')
        self.assertEqual(response_obj['description'],'Multiple services are down due to major network outage in our PHX1 data center')
        self.assertEqual(response_obj['severity']['id'],1)
        self.assertEqual(response_obj['severity']['name'],'Emergency')
        self.assertEqual(response_obj['posted_by'],'cshields')
        self.assertEqual(response_obj['admin_assigned'],'Rob Tucker')
        self.assertEqual(len(response_obj['service_outages_set']),2)
        self.assertEqual(response_obj['service_outages_set'][0],'/api/v1/serviceoutage/8/')
        self.assertEqual(response_obj['service_outages_set'][1],'/api/v1/serviceoutage/9/')

