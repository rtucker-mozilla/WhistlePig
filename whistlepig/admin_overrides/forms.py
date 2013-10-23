from django import forms
from whistlepig.whistlepig.models import SourceEmailAddress, DestinationEmailAddress
from whistlepig.whistlepig.models import StatusUpdate, OutageNotificationTemplate

class OutageNotificationForm(forms.Form):
    source_email_address = forms.ChoiceField(required=True)
    destination_email_address = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, required=True)
    subject = forms.CharField(max_length=128, widget=forms.TextInput(attrs={'size':'100'}))
    email_message = forms.CharField(widget=forms.Textarea(attrs={"rows":20, "cols":100}))

    def interpolate_template(self, template, status_update):
        template = template.replace('<<issue_status_description>>', status_update.summary)
        template = template.replace('<<issue_status>>', status_update.status.name)
        template = template.replace('<<bug_ids>>', status_update.bugzilla_id)
        template = template.replace('<<issue_date>>', status_update.start_time.strftime("%Y-%m-%d"))
        template = template.replace('<<issue_start_time>>', status_update.start_time.strftime("%H:%M UTC"))
        template = template.replace('<<issue_duration>>', str(status_update.duration_minutes))
        template = template.replace('<<services>>', ', '.join([s.service.name for s in status_update.serviceoutage_set.all()]))
        template = template.replace('<<summary>>', status_update.description)
        if status_update.site:
            template = template.replace('<<issue_site>>', status_update.site.name)
        return template

    def __init__(self, *args, **kwargs):
        status_update = kwargs.pop('status_update', None)
        outage_notification_template = kwargs.pop('outage_notification_template')
        email_template = outage_notification_template.interpolate_template(status_update = status_update)
        source_email_addresses = [['', '---Please Select---']]
        for s in SourceEmailAddress.objects.all():
            source_email_addresses.append([s.name,s.name])

        destination_email_addresses = []
        for s in DestinationEmailAddress.objects.all():
            destination_email_addresses.append([s.name,s.name])
        super(OutageNotificationForm, self).__init__(*args, **kwargs)
        self.fields['source_email_address'].choices = source_email_addresses
        self.fields['destination_email_address'].choices = destination_email_addresses
        if outage_notification_template.subject and outage_notification_template.subject != '':
            self.fields['subject'].initial = outage_notification_template.interpolate_subject(status_update = status_update)
        else:
            self.fields['subject'].initial = "[OUTAGE NOTIFICATION] %s" % status_update.summary
        self.fields['email_message'].initial = email_template


