from django.test import Client
from test_utils import TestCase, RequestFactory, setup_test_environment
setup_test_environment()
from django.core.urlresolvers import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from models import StatusUpdate, OutageNotificationTemplate
uninterpolated_template = u"""Mozilla  IT Operations Maintenance Notification:
----------------------------------------------------------------------
<<description>>
ISSUE STATUS:      <<status>>
BUG IDS:           <<bugzilla_id>>
DATE:              <<event_start_date>>
START TIME:        <<event_start_time>> <<timezone>>
DURATION:          <<duration_minutes>>
SITE:              <<site>>
SERVICES:          <<services>>
TYPE OF WORK:      <<type_of_work>>
IMPACT OF WORK:    <<summary>>    

If you have any questions or concerns please address them to
<<source_email_address>>
----------------------------------------------------------------------
<<source_description>> - <<source_email_address>>"""

interpolated_template = u"""Mozilla  IT Operations Maintenance Notification:
----------------------------------------------------------------------
<<issue_status_description>>
ISSUE STATUS:      <<status.name>>
BUG IDS:           <<bug_ids>>
DATE:              <<>>
START TIME:        <<issue_start_time>>
DURATION:          <<issue_duration>>
SITE:              <<issue_site>>
SERVICES:          <<services>>
TYPE OF WORK:      <<type_of_work>>
IMPACT OF WORK:    <<summary>>    

If you have any questions or concerns please address them to
<<source_email_address>>
----------------------------------------------------------------------
<<source_description>> - <<source_email_address>>"""

class HomePageTests(TestCase):
    fixtures = ['whistlepig']

    def setUp(self):
        self.client = Client()
        self.rf = RequestFactory()

    def test1_home_page(self):
        response = self.client.get(reverse("whistlepig.home"), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['updates']), 2)
        self.assertEqual(len(response.context['updates'][0]), 3)
        self.assertEqual(len(response.context['updates'][1]), 3)
        self.assertEqual(
                str(response.context['updates'][0]['articles'][0]),
                'test for july')


    def test2_home_page_contexts(self):
        response = self.client.get(reverse("whistlepig.home"), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['updates']), 2)
        self.assertEqual(len(response.context['updates'][0]), 3)
        self.assertEqual(len(response.context['updates'][1]), 3)
        self.assertEqual(
                str(response.context['updates'][0]['articles'][0]),
                'test for july')

    def test3_home_page_no_status_updates(self):
        StatusUpdate.objects.all().delete()
        response = self.client.get(reverse("whistlepig.home"), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['updates']), 0)

    def test4_outage_notification_template(self):
        on = OutageNotificationTemplate.objects.get(id=1)
        self.assertEqual(on.name, u'IT Maintenance Notification')

    def test5_detect_if_line_has_variable_false(self):
        on = OutageNotificationTemplate.objects.get(id=1)
        self.assertEqual(on.extract_variable_to_interpolate('asfdasfasfd'), None)

    def test6_detect_if_line_has_variable_true(self):
        on = OutageNotificationTemplate.objects.get(id=1)
        self.assertEqual(on.extract_variable_to_interpolate('bar<<site>>foo'), {
            '<<site>>': 'site',
            })
    def test6_detect_if_line_has_variable_true(self):
        on = OutageNotificationTemplate.objects.get(id=1)
        self.assertEqual(on.extract_variable_to_interpolate('a <<site>> word\r\n<<bar>>'), {
            '<<site>>': 'site',
            '<<bar>>':  'bar',
            })

    #def test7_test_proper_outage_notification_text(self):
    #    on = OutageNotificationTemplate.objects.get(id=1)
    #    self.assertEqual(on.outage_notification_template, uninterpolated_template)


    def test8_test_interpolated_hash_length(self):
        su = StatusUpdate.objects.get(id=6)
        on = OutageNotificationTemplate.objects.get(id=1)
        on.interpolate_template(status_update = su)
        interpolated_hash = on.interpolated_variable_hash
        self.assertEqual(len(interpolated_hash), 12)

    def test9_test_interpolated_hash_status(self):
        su = StatusUpdate.objects.get(id=6)
        on = OutageNotificationTemplate.objects.get(id=1)
        model_interpolated_template = on.interpolate_template(status_update = su,
                template = uninterpolated_template)
        test_string = 'ISSUE STATUS:      %s' % su.status.name
        self.assertTrue(test_string in model_interpolated_template)

    def test10_test_interpolated_hash_status(self):
        su = StatusUpdate.objects.get(id=6)
        on = OutageNotificationTemplate.objects.get(id=1)
        model_interpolated_template = on.interpolate_template(status_update = su,
                template = uninterpolated_template)
        test_string = 'ISSUE STATUS:      %s' % su.status.name
        self.assertTrue(test_string in model_interpolated_template)

    def test11_test_interpolated_hash_summary(self):
        su = StatusUpdate.objects.get(id=6)
        on = OutageNotificationTemplate.objects.get(id=1)
        model_interpolated_template = on.interpolate_template(status_update = su,
                template = uninterpolated_template)
        test_string = 'IMPACT OF WORK:    %s' % su.summary
        self.assertTrue(test_string in model_interpolated_template)

    def test12_test_interpolated_hash_start_date(self):
        su = StatusUpdate.objects.get(id=6)
        on = OutageNotificationTemplate.objects.get(id=1)
        model_interpolated_template = on.interpolate_template(status_update = su,
                template = uninterpolated_template)
        test_string = 'DATE:              %s' % su.event_start_date
        self.assertTrue(test_string in model_interpolated_template)

    def test13_test_interpolated_hash_start_time_with_timezone(self):
        su = StatusUpdate.objects.get(id=6)
        on = OutageNotificationTemplate.objects.get(id=1)
        model_interpolated_template = on.interpolate_template(status_update = su,
                template = uninterpolated_template)
        test_string = 'START TIME:        %s %s' % (su.event_start_time, su.timezone)
        self.assertTrue(test_string in model_interpolated_template)

    def test14_test_interpolated_hash_duration(self):
        su = StatusUpdate.objects.get(id=6)
        on = OutageNotificationTemplate.objects.get(id=1)
        model_interpolated_template = on.interpolate_template(status_update = su,
                template = uninterpolated_template)
        test_string = 'DURATION:          %s' % su.duration_minutes
        self.assertTrue(test_string in model_interpolated_template)

    def test15_test_interpolated_hash_site(self):
        su = StatusUpdate.objects.get(id=6)
        on = OutageNotificationTemplate.objects.get(id=1)
        model_interpolated_template = on.interpolate_template(status_update = su,
                template = uninterpolated_template)
        test_string = 'SITE:              %s' % su.site
        self.assertTrue(test_string in model_interpolated_template)

    def test16_test_interpolated_hash_duration(self):
        su = StatusUpdate.objects.get(id=6)
        on = OutageNotificationTemplate.objects.get(id=1)
        model_interpolated_template = on.interpolate_template(status_update = su,
                template = uninterpolated_template)
        test_string = 'BUG IDS:           %s' % su.bugzilla_id
        self.assertTrue(test_string in model_interpolated_template)

    def test17_test_interpolated_services(self):
        su = StatusUpdate.objects.get(id=6)
        on = OutageNotificationTemplate.objects.get(id=1)
        model_interpolated_template = on.interpolate_template(status_update = su,
                template = uninterpolated_template)
        test_string = 'SERVICES:          %s' % su.services
        self.assertTrue(test_string in model_interpolated_template)

    def test18_test_interpolated_summary(self):
        su = StatusUpdate.objects.get(id=6)
        on = OutageNotificationTemplate.objects.get(id=1)
        model_interpolated_template = on.interpolate_template(status_update = su,
                template = uninterpolated_template)
        test_string = 'IMPACT OF WORK:    %s' % su.summary
        self.assertTrue(test_string in model_interpolated_template)
