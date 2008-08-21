import datetime
from django.conf import settings
from django.contrib.sites.models import Site

from conescy.apps.stats.models import Day
from conescy.apps.stats.utils import *
from conescy.apps.stats.processor import process_request

class AddToStats(object):
    """Add current request to stats if it is 200! The response will not be manipulated! You can find the processor which takes the request data and saves it as a Conescy Stats dictionary in processor.process_request!"""
    
    def process_response(self, request, response):
        """Add the request data to the stats"""
        if not str(response.status_code) == '200':
            return response
        
        for path in settings.STATS_EXCLUDE:
            if path in request.path:
                return response
        
        day, created = Day.objects.get_or_create(date=datetime.date.today(), defaults={'stats': '{}', 'date': datetime.date.today()})
        
        # load the stats data
        stats = eval(day.stats)
        
        process_request(request, stats, {'site': Site.objects.get_current().domain})
        
        day.stats = str(stats)
        day.save()
        
        return response
