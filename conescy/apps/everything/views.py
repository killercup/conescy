import datetime

from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from django.views.generic.list_detail import object_list

from conescy.apps.everything.models import Entry

def author(request, author, app=False, **kwargs):
    """This view displays the public entries one author has written.
    
It uses the Generic View ``object_list`` and accepts all of its options. The only required argument is the author's username (called ``author``). To only display the entries of one Everything instance you can also pass the Everything-app as either an argument or a keyword argument (both called ``app``).
    
To use this for a feed template, just add ``rss: True`` as keyword argument and the feed's title, description and site will be set automatically. The view also passes two variables as ``extra_context`` to the template: ``author`` which contains the author's username (the required argument) and ``special``, which is usable as a heading ("All Articles by <author>")."""
    if app == False: app =  kwargs.pop("app")
    u = get_object_or_404(User, username=author)
    e = Entry.objects.filter(author=u, status="public", app=app).order_by("-created")
    
    if not kwargs.get("extra_context", False): kwargs["extra_context"] = {}
    kwargs["extra_context"]["special"] = "All Articles by %s" % author
    kwargs["extra_context"]["author"] = author
    
    if kwargs.pop("rss", False) == True:
        kwargs["extra_context"]["title"] = kwargs["extra_context"].get("name", "") + "Articles by %s" % author
        kwargs["extra_context"]["description"] = kwargs["extra_context"]["title"]
        kwargs["extra_context"]["site"] = Site.objects.get_current().domain
    
    return object_list(request, e, **kwargs)


def detail_comments(request, slug, app=False, **kwargs):
    """This view renders a page (e.g. a feed) with all (approved) comments made on an entry. This depends on Conescy's comments app, so be sure to have it in your ``INSTALLED_APPS``.
    
It uses the Generic View ``object_list`` and accepts all of its options. The only required argument is the entry's slug (called ``slug``). To only display the entries of one Everything instance you can also pass the Everything-app as either an argument or a keyword argument (both called ``app``).
    
To use this for a feed template, just add ``rss: True`` as keyword argument and the feed's title, description, link and site will be set automatically. The view also passes two variables as ``extra_context`` to the template: ``entry`` which contains the entry's slug (the required argument) and ``special``, which is usable as a heading ("Comment to <entry>")."""
    from conescy.apps.comments.models import Comment
    
    if app == False: app =  kwargs.pop("app")
    entry = get_object_or_404(Entry, slug=slug)
    
    cref = "%s.entry.%s" % (app, str(entry.id))
    comments = Comment.objects.filter(ref=cref, status='ok')
    for c in comments:
        c.get_the_title = "Comment #%i to %s" % (c.id, entry.title)
        
    if not kwargs.get("extra_context", False): kwargs["extra_context"] = {}
    kwargs["extra_context"]["special"] = 'Comment to "%s"' % entry.title
    kwargs["extra_context"]["entry"] = entry
    if kwargs.pop("rss", False) == True:
        kwargs["extra_context"]["title"] = kwargs["extra_context"].get("name", "") + 'Comment to "%s"' % entry.title
        kwargs["extra_context"]["description"] = kwargs["extra_context"]["title"]
        kwargs["extra_context"]["link"] = entry.get_absolute_url()
        kwargs["extra_context"]["site"] = Site.objects.get_current().domain
    
    return object_list(request, comments, **kwargs)


def comments(request, app=False, **kwargs):
    """This view renders a page (e.g. feed) with all (approved) comments for a specific app. This depends on Conescy's comments app, so be sure to have it in your ``INSTALLED_APPS``.
    
It uses the Generic View ``object_list`` and accepts all of its options. The only required argument is the Everything instance's name, which can also be given as keyword argument (both called ``app``).
    
To use this for a feed template, just add ``rss: True`` as keyword argument and the feed's title, description, link and site will be set automatically. The view also passes one variable as ``extra_context`` to the template, ``special``, which is usable as a heading ("Comments in <app>")."""
    from conescy.apps.comments.models import Comment
    
    if app == False: app =  kwargs.pop("app")
    comments = Comment.objects.filter(ref__startswith="%s." % app, status='ok')
    
    if not kwargs.get("extra_context", False): kwargs["extra_context"] = {}
    kwargs["extra_context"]["special"] = 'Comments in "%s"' % app.capitalize()
    if kwargs.pop("rss", False) == True:
        kwargs["extra_context"]["title"] = kwargs["extra_context"].get("name", "") + 'Comments in "%s"' % app.capitalize()
        kwargs["extra_context"]["description"] = kwargs["extra_context"]["title"]
        kwargs["extra_context"]["link"] = reverse("%s-home" % app)
        kwargs["extra_context"]["site"] = Site.objects.get_current().domain
    
    return object_list(request, comments, **kwargs)


@login_required
def import_rss(request, **kwargs):
    """View for executing the RSS import (found in everything.imports). This view requires the user to be logged in.
    
If data is POSTed to this view, this view will try to import that data will the RSS importer. If this view is requested via GET it will render a template (which should offer an option for importing data by POSTing it to this view).
    
This view does not require any direct arguments, but you can specify the templates used with keyword arguments:
    
- ``template_load`` defines the template used to POST the data to this import view, default is ``admin/importrss/load.html``. This template will also get the content variable ``users`` which will contain a QuerySet with all ``User`` objects (e.g. to generate the user list).
- ``template_finished`` defines the template used after importing the data, default is ``admin/importrss/finished.html``
    
The POSTed data should contain the following:
    
- the xml data in a field called ``xml``
- the name in which Everything instance to copy the entries in a field called ``instance``
- and the author's id which will set the author of all imported entries in a field called ``author``.
    """
    from conescy.apps.everything import imports
    
    if request.method == "POST":
        imports.rss(xml=request.FILES['rss'], instance=request.POST['instance'], author=request.POST['author'])
    
        template_finished = kwargs.get("template_finished", False) or "admin/importrss/finished.html"
    
        return render_to_response(template_finished, context_instance=RequestContext(request))
    
    else:
        users = User.objects.all()
        template_load = kwargs.get("template_load", False) or "admin/importrss/load.html"
        return render_to_response(template_load, {"users": users}, context_instance=RequestContext(request))


@login_required
def import_wordpress(request):
    """View for executing the Wordpress import (found in everything.imports). This is similar to RSS import but imports from Wordpress Export files instead (they contain some more information and all the comments!). This view requires the user to be logged in.
    
If data is POSTed to this view, this view will try to import that data will the Wordpress importer. If this view is requested via GET it will render a template (which should offer an option for importing data by POSTing it to this view).
    
This view does not require any direct arguments, but you can specify the templates used with keyword arguments:
    
- ``template_load`` defines the template used to POST the data to this import view, default is ``admin/importrss/load.html``. This template will also get the content variable ``users`` which will contain a QuerySet with all ``User`` objects (e.g. to generate the user list).
- ``template_finished`` defines the template used after importing the data, default is ``admin/importrss/finished.html``
    
The POSTed data should contain the following:
    
- the xml data of the Wordpress Export file in a field called ``xml``
- the name in which Everything instance to copy the entries in a field called ``instance``
- and the author's id which will set the author of all imported entries in a field called ``author``.
    """
    from conescy.apps.everything import imports
    
    if request.method == "POST":
        imports.wordpress(xml=request.FILES['xml'], instance=request.POST['instance'], author=request.POST['author'])
        template_finished = kwargs.get("template_finished", False) or "admin/importrss/finished.html"
        return render_to_response(template_finished, context_instance=RequestContext(request))
    else:
        users = User.objects.all()
        template_load = kwargs.get("template_load", False) or "admin/importrss/load.html"
        return render_to_response(template_load, {"users": users}, context_instance=RequestContext(request))


def tag_list(request, tag, app=False, **kwargs):
    """This view displays a list of public entries for one tag.
    
It uses the Generic View ``object_list`` and accepts all of its options. The only required argument is the tags's name (called ``tag`` of course). To only display the entries of one Everything instance you can also pass the Everything-app as either an argument or a keyword argument (both called ``app``).
    
To use this for a feed template, just add ``rss: True`` as keyword argument and the feed's title, description, link and site will be set automatically. The view also passes one variables as ``extra_context``, ``tag``, which contains the tags's name (the required argument)."""
    from tagging.models import Tag, TaggedItem
    
    if app == False: app =  kwargs.pop("app")
    
    t = get_object_or_404(Tag, name=tag)
    e = Entry.objects.select_related().filter(tags__contains=tag, status="public", app=app).order_by("-created")
    
    if not kwargs.get("extra_context", False): kwargs["extra_context"] = {}
    kwargs["extra_context"]["tag"] = tag
    if kwargs.pop("rss", False) == True:
        kwargs["extra_context"]["title"] = kwargs["extra_context"].get("name", "") + 'Tag "%s"' % (tag.capitalize())
        kwargs["extra_context"]["description"] = kwargs["extra_context"]["title"]
        kwargs["extra_context"]["link"] = reverse("tags-detail", args=[tag])
        kwargs["extra_context"]["site"] = Site.objects.get_current().domain
    
    return object_list(request, e, **kwargs)


def search(request, app=False, **kwargs):
    """This view displays a list of public entries that match a given search string.
    
It uses the Generic View ``object_list`` and accepts all of its options. The only required argument is the search string, which has to be passed as GET-Parameter called ``s`` (e.g. ``/search/?s=searchstring``). To only display the entries of one Everything instance you can also pass the Everything-app as either an argument or a keyword argument (both called ``app``).
    
This view also accepts two other keyword arguments:
    
- ``template_ajax`` to set the template used to display on ajax requests, default is ``search/results.html``
- ``template_name`` to set the template normally displayed, default is ``search/resultpage.html``
    
Fixme: Currently this view does not support pagination, because the ``?page=xx`` would override the ``?s=search`` search-string.
    """
    from django.db.models import Q
    
    if request.GET.get("s", False):
        s = request.GET["s"]
    else:
        # todo: add an error view!
        return render_to_response("error.html", {'error': 'You need to send a searchstring to search for something...'}, context_instance=RequestContext(request))
    
    if app == False: app =  kwargs.pop("app")
    
    if app:
        e = Entry.objects.select_related().filter(Q(app=app), Q(title__contains=s) | Q(content__contains=s))
    else:
        e = Entry.objects.select_related().filter(title__contains=s) & Entry.objects.filter(content__contains=s)
    
    if not kwargs.get("extra_context", False): kwargs["extra_context"] = {}
    kwargs["extra_context"]["search"] = s
    
    if request.is_ajax():
        template_ajax = kwargs.get("template_ajax", False) or "search/results.html"
        kwargs["template_name"] = template_ajax
        kwargs["paginate_by"] = None
        return object_list(request, e, **kwargs)
    else:
        if not kwargs.get("template_name", False): kwargs["template_name"] = "search/resultpage.html"
        return object_list(request, e, **kwargs)

