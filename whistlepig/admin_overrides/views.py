import commonware
from django.core.urlresolvers import reverse
from django.db.models import Q
import operator
from django.shortcuts import render
from whistlepig.whistlepig.models import StatusUpdate, SourceEmailAddress, OutageNotificationTemplate
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.shortcuts import  get_object_or_404
import datetime
from django.core.mail import send_mail
import json
import time
#log = commonware.log.getLogger('whistlepig')
import datetime
from django.contrib.admin.views.decorators import staff_member_required
from forms import OutageNotificationForm
from django.core.mail import EmailMultiAlternatives



@staff_member_required
def admin_send_outage_notification(request, id, template='admin_overrides/admin_outage_notification.html'):
    status_update = get_object_or_404(StatusUpdate, id=id)
    outage_notification_template_id = request.GET.get('notification_template', None)
    if outage_notification_template_id:
        outage_notification_template = OutageNotificationTemplate.objects.get(id=outage_notification_template_id)
    else:
        outage_notification_template = None

    outage_notification_templates = OutageNotificationTemplate.objects.all()
    source_email_address_objects = SourceEmailAddress.objects.all()
    source_email_addresses = {}
    for s in source_email_address_objects:
        source_email_addresses[s.name] = s.short_description
    source_email_addresses = json.dumps(source_email_addresses);
    message = None
    if request.method == 'POST':
        outage_notification_template = OutageNotificationTemplate.objects.get(id=request.POST.get('outage_notification_template_id'))
        form = OutageNotificationForm(request.POST, status_update=status_update, outage_notification_template=outage_notification_template)
        if form.is_valid():
            cleaned_data = form.clean()
            destination_email_address = cleaned_data['destination_email_address']
            email_message = cleaned_data['email_message']
            subject = cleaned_data['subject']
            text_content = email_message
            html_message = """<html>
            <head>
            <style type='text/css'>
            pre {
                white-space: pre-wrap; /* css-3 /
                white-space: -moz-pre-wrap; / Mozilla, since 1999 /
                white-space: -pre-wrap; / Opera 4-6 /
                white-space: -o-pre-wrap; / Opera 7 /
                word-wrap: break-word; / Internet Explorer 5.5+ */
                font-family: monospace;
            }
            </style>
            </head><body><pre>%s</pre></body></html>""" % text_content
            source_email_address = cleaned_data['source_email_address']
            msg = EmailMultiAlternatives(subject, text_content, source_email_address, destination_email_address)
            msg.attach_alternative(html_message, "text/html")
            msg.send()
            message = 'Outage Notification Sent'
    elif outage_notification_template_id:
        form = OutageNotificationForm(status_update=status_update, outage_notification_template=outage_notification_template)
    else:
        form = None
    return render_to_response(template,
            {
                'form': form,
                'outage_notification_templates': outage_notification_templates,
                'outage_notification_template_id': outage_notification_template_id,
                'message': message,
                'source_email_addresses': source_email_addresses,
            },
              context_instance=RequestContext(request))

