from django.conf.urls.defaults import *

from conescy.apps.wiki.models import Page
wiki_dict = {'queryset': Page.objects.filter(status="public").order_by('name'),}

urlpatterns = patterns('',
    url(r'^$', 'django.views.generic.simple.redirect_to', {'url': '/wiki/Start/'}, name="wiki-home"),
    url(r'^toc/$', 'django.views.generic.list_detail.object_list', dict(wiki_dict, paginate_by=30, template_name="wiki/page_list.html"), name="wiki-toc"),
    url(r'^(?P<name>.*)/edit/$', 'conescy.apps.wiki.views.edit', name="wiki-edit"),
    url(r'^(?P<name>.*)/revisions/$', 'conescy.apps.wiki.views.revs', name="wiki-revs"),
    url(r'^(?P<name>.*)/rev(?P<revno>.*)/$', 'conescy.apps.wiki.views.onerev', name="wiki-revision"),
    url(r'^(?P<name>.*)/$', 'conescy.apps.wiki.views.page', name="wiki-page"),
)
