import datetime
from urlparse import urlparse
from django.conf import settings
from django.contrib.sites.models import Site

from conescy.apps.stats.models import Day
from conescy.apps.stats.utils import *

class AddToStats(object):
    """Add current request to stats if it is 200! The response will not be manipulated!
This will add the following information as a python dict to th model:

- for bots (have a look at utils.is_bot): just a counter how many bot-hits has been made
- for ajax hits (uses request.is_ajax()): also just a counter
- for feed/site hits:
 - a counter of hits (seperated for site/feed)
 - a list of IP's to determinate unique visitors (seperated for site/feed)
 - a dict of different user agents and the number of their uses (seperated for site/feed)
 - a dict of paths and a counter of their requests (seperated for site/feed)
 - a dict of referrers and their uses ("internal" for internal referrers, this is for site hits only, of course)
 - a dict of search strings and their uses (if the refer is from a search engine, uses utils.is_search, also for site hits only)
 - a counter of hits by "user", visitors with cookies (real users or just commenters)
    """
    
    def process_response(self, request, response):
        """Add the request data to the stats"""
        if not str(response.status_code) == '200':
            return response
        
        for path in settings.STATS_EXCLUDE:
            if path in request.path:
                return response
        
        day, created = Day.objects.get_or_create(date=datetime.date.today(), defaults={'stats': '{}', 'date': datetime.date.today()})
        site = Site.objects.get_current().domain
        
        # load the stats data
        stats = eval(day.stats)
        
        # is the visitor a bot?
        if is_bot(request.META.get("HTTP_USER_AGENT", "")):
            stats["bots"] = stats.get("bots", 0) + 1
            day.stats = str(stats)
            day.save()
            return response
        # is this an ajax request?
        elif request.is_ajax():
            stats["ajax"] = stats.get("ajax", 0) + 1
            day.stats = str(stats)
            day.save()
            return response
        # is a feed requested
        elif is_feed(request.path):
            stats["feeds"] = stats.get("feeds", 0) + 1
            ips = stats.get("feed_ips", [])
            paths = stats.get("feed_paths", {})
        # normal hits
        else:
            stats["hits"] = stats.get("hits", 0) + 1
            ips = stats.get("ips", [])
            paths = stats.get("paths", {})
            
            browser_engine = stats.get("browser_engine", {})
            if 'khtml' in request.META.get("HTTP_USER_AGENT", "").lower():
                browser_engine["KHTML"] = browser_engine.get("KHTML", 0) + 1
            elif 'gecko' in request.META.get("HTTP_USER_AGENT", "").lower():
                browser_engine["Gecko"] = browser_engine.get("Gecko", 0) + 1
            elif 'msie' in request.META.get("HTTP_USER_AGENT", "").lower():
                browser_engine["MSIE"] = browser_engine.get("MSIE", 0) + 1
            elif 'opera' in request.META.get("HTTP_USER_AGENT", "").lower():
                browser_engine["Opera"] = browser_engine.get("Opera", 0) + 1
            else:
                browser_engine["other"] = browser_engine.get("other", 0) + 1
        
        # paths: paths of requested pages/feeds
        paths[site+request.path] = paths.get(site+request.path, 0) + 1
        
        # list of ip's
        if not request.META.get("REMOTE_ADDR", "") in ips:
            ips.append(request.META.get("REMOTE_ADDR", ""))
        
        # lits of operating systems
        os = stats.get("os", {})
        if 'windows' in request.META.get("HTTP_USER_AGENT", "").lower():
            os["windows"] = os.get("windows", 0) + 1
        elif 'os x' in request.META.get("HTTP_USER_AGENT", "").lower():
            os["osx"] = os.get("osx", 0) + 1
        elif 'linux' in request.META.get("HTTP_USER_AGENT", "").lower():
            os["linux"] = os.get("linux", 0) + 1
        
        # refers
        if request.META.get("HTTP_REFERER", False) != False:
            refs = stats.get("refs", {})
            ref = urlparse(request.META["HTTP_REFERER"])
            
            if ref[1] == site:
                refs["internal"] = refs.get("internal", 0) + 1
            else:
                refs[ref[1]] = refs.get(ref[1], 0) + 1
            
            stats["refs"] = refs
            
            s = is_search(ref, return_query=True)
            # if ths user comes from a search engine
            if s:
                searchs = stats.get("searchs", {})
                searchs[s.lower()] = searchs.get(s.lower(), 0) + 1
                
                stats["searchs"] = searchs
        
        if request.user.is_authenticated():
            stats["user_hits"] = stats.get("user_hits", 0) + 1
        
        # save the stats data
        if is_feed(request.path):
            stats["feed_paths"] = paths
            stats["feed_ips"] = ips
        else:
            stats["paths"] = paths
            stats["ips"] = ips
            stats["browser_engine"] = browser_engine
        stats["os"] = os
        day.stats = str(stats)
        day.save()
        
        return response
