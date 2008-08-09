from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # save comments (only accepts POST)
    url(r'save/$', 'conescy.apps.comments.views.save', name="comments-save"),
    # delete comments, variable should be the comment's id
    url(r'^delete/(?P<comment>.*)/$', 'conescy.apps.comments.views.delete', name="comments-delete"),
)