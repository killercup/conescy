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
    """Displays the articles one author has written"""
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
    """A page (feed) with all comments made for an article. This depends on Conescy's comments app."""
    from conescy.apps.comments.models import Comment
    
    if app == False: app =  kwargs.pop("app")
    entry = get_object_or_404(Entry, slug=slug)
    
    cref = "%s.entry.%s" % (app, str(entry.id))
    comments = Comment.objects.filter(ref=cref)
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
    """A page (feed) with all comments for a specific app. Depends on Conescy's comments app."""
    from conescy.apps.comments.models import Comment
    
    if app == False: app =  kwargs.pop("app")
    comments = Comment.objects.filter(ref__startswith="%s." % app)
    
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
    """View for executing the RSS import (found in everything.imports)."""
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
    """View for executing the Wordpress import (found in everything.imports)."""
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
    """A list of entries for a tag, requires a keywordargument to know which everything instance should be used."""
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


def search(request, **kwargs):
    """A really simple (and generic) search engine. Add 'app' as a keyword-argument if you want to use this for one app only."""
    from django.db.models import Q
    
    if request.GET.get("s", False):
        s = request.GET["s"]
    else:
        # todo: add an error view!
        return render_to_response("error.html", {'error': 'You need to send a searchstring to search for something...'}, context_instance=RequestContext(request))
    
    app = kwargs.get("app", False)
    
    if app:
        e = Entry.objects.select_related().filter(Q(app=app), Q(title__contains=s) | Q(content__contains=s))
    else:
        e = Entry.objects.select_related().filter(title__contains=s) & Entry.objects.filter(content__contains=s)
    
    if request.is_ajax():
        template_ajax = kwargs.get("template_ajax", False) or "search/results.html"
        return render_to_response(template_ajax, {'object_list': e, 'search': s}, context_instance=RequestContext(request))
    else:
        return object_list(request, e, **kwargs)

