from django.test import Client
from test_utils import TestCase, RequestFactory, setup_test_environment
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from .models import get_dest_emails
import json


class AdminOverrideTest(TestCase):
    fixtures = ['whistlepig']
    admin_user = 'admin'
    admin_pass = 'admin'

    def setUp(self):
        self.client = Client()
        self.rf = RequestFactory()
        admin_user = User.objects.create_user(self.admin_user, 'admin_user@domain.com', self.admin_pass)
        admin_user.is_superuser = True
        admin_user.is_staff = True
        admin_user.is_active = True
        admin_user.save()

    def tearDown(self):
        User.objects.all().delete()


    def test1_get_api_endpoint(self):
        self.client.login(username=self.admin_user, password=self.admin_pass)
        response = self.client.get('/admin/statusupdate/sendoutagenotification/11/?notification_template=1', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('additional_email_addresses' in response.context['form'].fields)

    def test2_get_dest_emails_with_additional_emails_none(self):
        ret_emails = get_dest_emails('foo@bar.com', None)
        self.assertEqual(ret_emails, ['foo@bar.com'])

    def test3_get_dest_emails_with_additional_emails_empty(self):
        ret_emails = get_dest_emails('foo@bar.com', [])
        self.assertEqual(ret_emails, ['foo@bar.com'])

    def test4_get_dest_emails_with_additional_emails_blank(self):
        ret_emails = get_dest_emails('foo@bar.com', '')
        self.assertEqual(ret_emails, ['foo@bar.com'])

    def test5_get_dest_emails_with_additional_emails(self):
        # Check for a single additional email
        ret_emails = get_dest_emails('foo@bar.com', 'abc@foo.com')
        self.assertEqual(ret_emails, ['foo@bar.com', 'abc@foo.com'])

        # Check for multiple emails separated by a space
        ret_emails = get_dest_emails('foo@bar.com',
                                     'abc@foo.com, abc2@foo.com')
        self.assertEqual(ret_emails, ['foo@bar.com',
                                      'abc@foo.com',
                                      'abc2@foo.com'])

        # Check for multiple emails separated by multiple spaces
        ret_emails = get_dest_emails('foo@bar.com','abc@foo.com,   abc2@foo.com,'
                                                   'abc3@foo.com')
        self.assertEqual(ret_emails, ['foo@bar.com',
                                      'abc@foo.com',
                                      'abc2@foo.com',
                                      'abc3@foo.com'])

        # Check for multiple emails not separated by a space
        ret_emails = get_dest_emails('foo@bar.com', 'abc@foo.com,abc2@foo.com')
        self.assertEqual(ret_emails, ['foo@bar.com', 'abc@foo.com', 'abc2@foo.com'])
