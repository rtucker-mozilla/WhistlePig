import commonware

from django.shortcuts import render
from models import StatusUpdate
from django.http import HttpResponse
from django.shortcuts import  get_object_or_404

log = commonware.log.getLogger('whistlepig')
import datetime
def detail(request, id, template='whistlepig/detail.html'):
    status_update = get_object_or_404(StatusUpdate, pk=id)
    data = {
            'article': status_update,
            }

    return render(request, template, data)
def home(request, template='whistlepig/home.html'):
    """Main landing page for whistlepig"""
    total_months_to_show = 5
    home_results = []
    """
        Get the most recent month of results. This
        will be the baseline for other months
    """
    most_recent = StatusUpdate.objects.all().order_by('-posted_on')[1]
    home_results.append({
        'month_name': most_recent.posted_on.strftime("%B"),
        'articles': get_results_by_month_year(most_recent.posted_on.month, most_recent.posted_on.year)
        })

    """
        Iterate over previous months up to
        total_months_to_show and add them
        to the results list if not None
    """

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

