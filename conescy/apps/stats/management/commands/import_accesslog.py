from django.core.management.base import BaseCommand, CommandError
from conescy.apps.stats import logimport

class Command(BaseCommand):
    """Import from an access log (apache or lighttpd) into Conescy Stats."""
    
    help = __doc__
    args = "[path]"
    label = 'access log path'
    requires_model_validation = False
    
    def handle(self, path, **options):
        print 'Start importing "%s"' % path
        # open file
        f = file(path, 'r')
        try:
            a = logimport.logimport(f)
            if a == True:
                print 'Finished Importing "%s"' % path
        except:
            print "Damn! Got an error during import..."
    
