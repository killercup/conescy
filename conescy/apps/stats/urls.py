from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^statz/(?P<date>.*)/$', 'conescy.apps.stats.views.day', name="stats-day"),
    url(r'^statz/$', 'conescy.apps.stats.views.home', name="stats-home"),
)