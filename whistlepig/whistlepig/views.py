import commonware
from django.core.urlresolvers import reverse
from django.db.models import Q
import operator
from django.shortcuts import render
from models import StatusUpdate
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.shortcuts import  get_object_or_404
import datetime
import json
import time
#log = commonware.log.getLogger('whistlepig')
import datetime
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def admin_send_outage_notification(request, id, template='whistlepig/admin_outage_notification.html'):
    data = {}
    return render_to_response(template,
              context_instance=RequestContext(request))

def detail(request, id, template='whistlepig/detail.html'):
    status_update = get_object_or_404(StatusUpdate, pk=id)
    data = {
            'article': status_update,
            }

    return render(request, template, data)
def event_feed(request):
    start_time = request.GET.get('start', None)
    end_time = request.GET.get('end', None)

    try:
        start_query = (datetime.datetime.fromtimestamp(int(start_time)).strftime('%Y-%m-%d'))
        end_query = (datetime.datetime.fromtimestamp(int(end_time)).strftime('%Y-%m-%d'))
    except TypeError:
        return HttpResponse('You must supply a start and end timestamp')

    events = StatusUpdate.objects.filter(start_time__gte=start_query).filter(start_time__lte=end_query)
    if request.user.is_anonymous():
        events = events.filter(is_private = False)
    out_events = []
    for event in events:
        # Want to tie this into the backend at some point
        # Probably add an event.severity.color_name
        if event.severity.name == 'Emergency':
            event_color = 'red'
        elif event.severity.name== 'No Downtime':
            event_color = 'green'
        else:
            event_color = 'orange'

        start_time = int(time.mktime(event.start_time.timetuple()))
        end_time = int(time.mktime(event.start_time.timetuple()))

        out_events.append({
            'title': event.summary,
            'id': int(event.id),
            'url': '/detail/%s' % event.id,
            'color': event_color,
            'start': '"%s"' % (start_time),
            'end': '"%s"' % (end_time),
            })
    return HttpResponse(json.dumps(out_events))

def calendar(request, template='whistlepig/calendar.html'):
    data = {}
    search = request.POST.get('search', None)
    if search:
        filters = [Q(**{"%s__icontains" % t: search})
                        for t in StatusUpdate.search_fields]

        search_results = StatusUpdate.objects.filter(
                    reduce(operator.or_, filters)).distinct()
        if request.user.is_anonymous():
            search_results = search_results.filter(is_private = False)
        data['search_results'] = search_results
    return render(request, template, data)

def search(request, template='whistlepig/search.html'):
    data = {}
    search = request.POST.get('search', None)
    if search:
        filters = [Q(**{"%s__icontains" % t: search})
                        for t in StatusUpdate.search_fields]

        search_results = StatusUpdate.objects.filter(reduce(operator.or_, filters)).distinct()
        if request.user.is_anonymous():
            search_results = search_results.filter(is_private = False)
    data['search_results'] = search_results
    return render(request, template, data)

def home(request, template='whistlepig/home.html'):
    """Main landing page for whistlepig"""
    total_months_to_show = 5
    status_updates_found = False
    home_results = []
    """
        Get the most recent month of results. This
        will be the baseline for other months
    """
    try:
        if request.user.is_anonymous():
            most_recent = StatusUpdate.objects.all().filter(frontpage = True).filter(is_private = False).order_by('-start_time')[0]
        else:
            most_recent = StatusUpdate.objects.all().filter(frontpage = True).order_by('-start_time')[0]

        status_updates_found = True
    except IndexError:
        """
            There are no status updates
        """
        most_recent = False

    if status_updates_found:
        home_results.append({
            'month_name': most_recent.start_time.strftime("%B"),
            'month_year': most_recent.start_time.strftime("%Y"),
            'articles': get_results_by_month_year(most_recent.start_time.month, most_recent.start_time.year, request.user)
            })

    """
        Check if we have a most_recent article. If so then:

        Iterate over previous months up to
        total_months_to_show and add them
        to the results list if not None
    """
    if most_recent:
        for i in range(1, total_months_to_show):
            the_month = monthdelta(most_recent.start_time, -i)
            month_results = get_month_of_results(the_month, request.user)
            if month_results and not month_results['month_name'] in [m['month_name'] for m in home_results]:
                home_results.append(month_results)
    data = {}
    data['updates'] = home_results
    return render(request, template, data)

#def rss(request, template='whistlepig/home.html'):

def get_results_by_month_year(month, year, user):
    all_articles = StatusUpdate.objects.filter(frontpage = True).filter(start_time__year=year, start_time__month=month).order_by('start_time')

    if user.is_anonymous():
        all_articles = all_articles.filter(is_private = False)
    return all_articles

def get_month_of_results(current_month, user):

    try:
        if user.is_anonymous():
            most_recent = StatusUpdate.objects.filter(frontpage = True).filter(start_time__lte=current_month).filter(is_private = False).order_by('-start_time')[0]
        else:
            most_recent = StatusUpdate.objects.filter(frontpage = True).filter(start_time__lte=current_month).order_by('-start_time')[0]
    except IndexError:
        ### No results for this page
        return None

    ret_data = {
        'month_name': most_recent.start_time.strftime("%B"),
        'month_year': most_recent.start_time.strftime("%Y"),
        'articles': get_results_by_month_year(most_recent.start_time.month, most_recent.start_time.year, user)
        }
    return ret_data

def monthdelta(date, delta):
    m, y = (date.month+delta) % 12, date.year + ((date.month)+delta-1) // 12
    if not m: m = 12
    d = min(date.day, [31,
        29 if y%4==0 and not y%400==0 else 28,31,30,31,30,31,31,30,31,30,31][m-1])
    return date.replace(day=d,month=m, year=y)

