from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()

from conescy.apps.everything.models import Entry
blog_query = {'queryset': Entry.objects.filter(app="blog", status="public").order_by('-created'),}

urlpatterns = patterns('',
    # Example Blog:
    url(r'^$', 'django.views.generic.list_detail.object_list', dict(blog_query, paginate_by=10), name="blog-home"),
    url(r'^blog/(?P<slug>.*)/$', 'django.views.generic.list_detail.object_detail', dict(blog_query, slug_field='slug'), name="blog-detail"),
    
    # Example Wiki:
    (r'^wiki/', include('conescy.apps.wiki.urls')),
    
    # Conescy.Stats
    (r'^admin/', include('conescy.apps.stats.urls')),
    
    # Uncomment the next line to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    
    # Uncomment the next line for to enable the admin:
    (r'^admin/(.*)', admin.site.root),
)
