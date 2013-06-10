import commonware
from django.core.urlresolvers import reverse
from django.db.models import Q
import operator
from django.shortcuts import render
from models import StatusUpdate
from django.http import HttpResponse
from django.shortcuts import  get_object_or_404
import datetime
import json
import time
#log = commonware.log.getLogger('whistlepig')
import datetime
def detail(request, id, template='whistlepig/detail.html'):
    status_update = get_object_or_404(StatusUpdate, pk=id)
    data = {
            'article': status_update,
            }

    return render(request, template, data)
def event_feed(request):
    start_time = request.GET.get('start', None)
    end_time = request.GET.get('end', None)
    start_query = (datetime.datetime.fromtimestamp(int(start_time)).strftime('%Y-%m-%d'))
    end_query = (datetime.datetime.fromtimestamp(int(end_time)).strftime('%Y-%m-%d'))
    events = StatusUpdate.objects.filter(posted_on__gte=start_query).filter(posted_on__lte=end_query)
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
        
        out_events.append({
            'title': event.summary,
            'id': int(event.id),
            'url': '/detail/%s' % event.id,
            'color': event_color,
            'start': '"%s"' % (int(time.mktime(event.created_on.timetuple()))),
            'end': '"%s"' % (int(time.mktime(event.created_on.timetuple()))),
            })
    return HttpResponse(json.dumps(out_events))

def calendar(request, template='whistlepig/calendar.html'):
    data = {}
    search = request.POST.get('search', None)
    if search:
        filters = [Q(**{"%s__icontains" % t: search})
                        for t in StatusUpdate.search_fields]

        data['search_results'] = StatusUpdate.objects.filter(
                    reduce(operator.or_, filters)).distinct()
    return render(request, template, data)

def search(request, template='whistlepig/search.html'):
    data = {}
    search = request.POST.get('search', None)
    if search:
        filters = [Q(**{"%s__icontains" % t: search})
                        for t in StatusUpdate.search_fields]

        data['search_results'] = StatusUpdate.objects.filter(
                    reduce(operator.or_, filters)).distinct()
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
        most_recent = StatusUpdate.objects.all().order_by('-posted_on')[1]
        status_updates_found = True
    except IndexError:
        """
            There are no status updates
        """
        most_recent = False
        pass
    if status_updates_found:
        home_results.append({
            'month_name': most_recent.posted_on.strftime("%B"),
            'articles': get_results_by_month_year(most_recent.posted_on.month, most_recent.posted_on.year)
            })

    """
        Check if we have a most_recent article. If so then:

        Iterate over previous months up to
        total_months_to_show and add them
        to the results list if not None
    """
    if most_recent:
        for i in range(1, total_months_to_show):
            the_month = monthdelta(most_recent.posted_on, -i)
            month_results = get_month_of_results(the_month)
            if month_results and not month_results['month_name'] in [m['month_name'] for m in home_results]:
                home_results.append(month_results)
    data = {}
    data['updates'] = home_results
    return render(request, template, data)

#def rss(request, template='whistlepig/home.html'):

def get_results_by_month_year(month, year):
    return StatusUpdate.objects.filter(posted_on__year=year, posted_on__month=month)

def get_month_of_results(current_month):

    try:
        most_recent = StatusUpdate.objects.filter(posted_on__lt=current_month).order_by('-posted_on')[1]
    except IndexError:
        ### No results for this page
        return None
    
    ret_data = {
        'month_name': most_recent.posted_on.strftime("%B"),
        'articles': get_results_by_month_year(most_recent.posted_on.month, most_recent.posted_on.year)
        }
    return ret_data

def monthdelta(date, delta):
    m, y = (date.month+delta) % 12, date.year + ((date.month)+delta-1) // 12
    if not m: m = 12
    d = min(date.day, [31,
        29 if y%4==0 and not y%400==0 else 28,31,30,31,30,31,31,30,31,30,31][m-1])
    return date.replace(day=d,month=m, year=y)

