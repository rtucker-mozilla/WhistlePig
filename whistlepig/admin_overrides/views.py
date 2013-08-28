import commonware
from django.core.urlresolvers import reverse
from django.db.models import Q
import operator
from django.shortcuts import render
from whistlepig.whistlepig.models import StatusUpdate
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


@staff_member_required
def admin_send_outage_notification(request, id, template='admin_overrides/admin_outage_notification.html'):
    status_update = get_object_or_404(StatusUpdate, id=id)
    if request.method == 'POST':
        form = OutageNotificationForm(request.POST, status_update=status_update)
        if form.is_valid():
            cleaned_data = form.clean()
            destination_email_address = cleaned_data['destination_email_address']
            source_email_address = cleaned_data['source_email_address']
            send_mail(cleaned_data['subject'], cleaned_data['email_message'], source_email_address, [destination_email_address])
    else:
        form = OutageNotificationForm(status_update=status_update)
    return render_to_response(template,
            {
                'form': form,
                status_update: status_update,
            },
              context_instance=RequestContext(request))

