import time

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

from conescy.apps.stats.models import *

@login_required
def day(request, date):
    """stats for a single day"""
    d = Day.objects.get(date=date)
    stats = d.the_stats()
    
    site_paths = sorted(stats.get("paths", {}).iteritems(), key=lambda (k,v):(v,k), reverse=True)
    feed_paths = sorted(stats.get("feed_paths", {}).iteritems(), key=lambda (k,v):(v,k), reverse=True)
    
    refs = sorted(stats.get("refs", {}).iteritems(), key=lambda (k,v):(v,k), reverse=True)
    
    searchs = sorted(stats.get("searchs", {}).iteritems(), key=lambda (k,v):(v,k), reverse=True)
    anonymous_hits = stats.get("hits", 0) - stats.get("user_hits", 0)
    if anonymous_hits < 0: anonymous_hits = 0
    
    os = sorted(stats.get("os", {}).iteritems(), key=lambda (k,v):(v,k), reverse=True)
    browser_engine = sorted(stats.get("browser_engine", {}).iteritems(), key=lambda (k,v):(v,k), reverse=True)
    
    return render_to_response("stats/day.html", {'stats': stats, 'date': d.date, 'title': d, 'site_paths': site_paths, 'feed_paths': feed_paths, 'refs': refs, 'searchs': searchs, 'anonymous_hits': anonymous_hits, 'os': os, 'browser_engine': browser_engine}, context_instance=RequestContext(request))

@login_required
def home(request):
    """home page of stats, display some cool progression"""
    days = Day.objects.order_by("-date")[:14]
    site_hits = []
    site_visitors = []
    feed_hits = []
    feed_visitors = []
    paths = {}
    i = 0
    for day in days:
        stats = day.the_stats()
        site_hits.append([time.mktime(day.date.timetuple())*1000, int(stats.get("hits", 0))])
        site_visitors.append([time.mktime(day.date.timetuple())*1000, len(stats.get("ips", []))])
        feed_hits.append([time.mktime(day.date.timetuple())*1000, int(stats.get("feeds", 0))])
        feed_visitors.append([time.mktime(day.date.timetuple())*1000, len(stats.get("feed_ips", []))])
        pp = stats.get("paths", {})
        for p in pp.keys():
            paths[p] = paths.get(p, 0) + pp[p]
        i = i+1
    
    paths = sorted(paths.iteritems(), key=lambda (k,v):(v,k), reverse=True)
    
    return render_to_response("stats/home.html", {'site_hits': str(site_hits), 'site_visitors': str(site_visitors), 'feed_hits': str(feed_hits), 'feed_visitors': str(feed_visitors), 'days': days, 'title': 'Statz', 'paths': paths}, context_instance=RequestContext(request))
