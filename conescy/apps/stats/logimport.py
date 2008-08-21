import sys, re
from dateutil.parser import parse

from django.conf import settings

from conescy.apps.stats.models import Day
from conescy.apps.stats.processor import process_request

class Request(object):
    """Just a dummy. But it behaves like a Django request object!"""
    def __init__(self, r):
        self.path = r.group("path")
        self.method = r.group("method")
        self.status_code = r.group("status")
        self.META = {
            'HTTP_REFERER': r.group("refer"), 
            'HTTP_USER_AGENT': r.group("useragent"), 
            'REMOTE_ADDR': r.group("ip"), 
            'REQUEST_METHOD': r.group("method").upper(),
        }
    class user(object):
        def is_authenticated(self=False):
            return False
    user = user()
    def is_ajax(self=False):
        return False

# Set your access log format here.
# THIS is my longest fucking re code that works!!!
format = r'(?P<ip>[0-9.]*) (?P<domain>[a-zA-Z0-9.]*) - \[(?P<date>[0-9a-zA-Z/]*):(?P<time>[0-9:]*) (?P<timezone>[0-9+]*)\] "(?P<method>[A-Z]*) (?P<path>.*?) (?P<protocol>[0-9A-Z/.]*)" (?P<status>[0-9]*) (?P<process>[0-9-]*) "(?P<refer>.*?)" "(?P<useragent>.*?)"'

def loginit(s, day):
    """Load the date already in the db for the days we would like to import."""
    days = Day.objects.filter(date__gt=day)
    for d in days:
        if d.stats == "": d.stats = "{}"
        s[str(d.date)] = eval(d.stats)
    return s

def logparse(logfile):
    """Import an Apache or Lighttpd access log and save it for Conescy Stats. 
    
Currently, you cannot specify any format, it will just parse assuming it's in Apache's default format. This is e.g. something like that::

    91.13.116.4 pascalhertleif.de - [28/Jun/2008:20:29:39 +0000] "GET / HTTP/1.1" 200 3675 "http://killercup.de/?page=2" "Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9) Gecko/2008052906 Firefox/3.0"

    'ip domain - [Date:Time timezone] "METHODE path PROTOCOL/VERSION" statuscode processnumber "refer" "UserAgent"'

Also, if you send larger files to this function, it can take some time to process it all.
    """
    
    # let there be a dict.
    s = {}
    i = False
    
    for line in logfile:
        # parse this, snake!!
        r = re.search(format, line)
        
        # should I really have a look at this line?
        if r.group("path").startswith(settings.STATS_EXCLUDE):
            # - no, if path is excluded by setting
            continue
        
        if not str(r.group("status")) == '200':
            # - no, if the request returned an error
            continue
        
        day = parse(r.group("date")).date()
        
        # on the first run of each day, load 's' from the db
        if not i == str(day):
            s = loginit(s, day)
        
        # make a Django request object
        request = Request(r)
        
        if not s.get(str(day), False): s[str(day)] = {}
        s[str(day)] = process_request(request, s[str(day)])
        del request
        
        i = True
    return s

def logimport(logfile):
    """Parse the log file with ``logparse`` and save it in the database."""
    s = logparse(logfile)
    for key in s.keys():
        d = Day.objects.get_or_create(date=str(key), defaults={'date': str(key)})
        d[0].stats = str(s[key])
        d[0].save()
    
    return True
