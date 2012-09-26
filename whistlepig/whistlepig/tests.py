from django.test import Client
from test_utils import TestCase, RequestFactory, setup_test_environment
setup_test_environment()
from django.core.urlresolvers import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User

class HomePageTests(TestCase):
    fixtures = ['whistlepig']

    def setUp(self):
        self.client = Client()
        self.rf = RequestFactory()

    def test1_home_page(self):
        response = self.client.get(reverse("whistlepig.home"), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['updates']), 2)
        self.assertEqual(len(response.context['updates'][0]), 2)
        self.assertEqual(len(response.context['updates'][1]), 2)
        self.assertEqual(
                str(response.context['updates'][0]['articles'][0]),
                'Vidyo Maintenance Notice')


    def test2_home_page_contexts(self):
        response = self.client.get(reverse("whistlepig.home"), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['updates']), 2)
        self.assertEqual(len(response.context['updates'][0]), 2)
        self.assertEqual(len(response.context['updates'][1]), 2)
        self.assertEqual(
                str(response.context['updates'][0]['articles'][0]),
                'Vidyo Maintenance Notice')
