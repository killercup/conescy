import re

from django.http import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.views.generic.list_detail import object_list

from conescy.apps.wiki.models import Page, Revision

def page(request, name):
    """display a page -- or, if the page is unavailable a creation form. todo: doc"""
    try:
        page = Page.objects.get(name=name)
        
        if (page.status != 'public') and (not request.user.is_authenticated()):
            return render_to_response('error.html', {'error': "You are not allowed to view this page!",}, context_instance=RequestContext(request))
        
        # simple redirect of pages with a syntax like this: %redirect:"WikiSeite"%
        redirects = re.findall("%redirect:\"(.*)\"%", page.content)
        if len(redirects) > 0:
            from django.core.urlresolvers import reverse
            return HttpResponseRedirect(reverse('wiki-page', args=[redirects[0]]))
        else:
            return render_to_response('wiki/page.html', {'object': page,}, context_instance=RequestContext(request))
    except Page.DoesNotExist:
        return HttpResponseRedirect("%sedit/" % request.path)


@login_required
def edit(request, name):
    """Edit a wiki site (this also works for ajax edit!). todo: doc"""
    try:
        page = Page.objects.get(name=name)
        newpage = False
        oldcontent = page.content
    except Page.DoesNotExist:
        page = Page(name=name)
        newpage = True
    
    if request.method == "POST":
        page.tags = request.POST['tags']
        page.status = "public"
        page.content = request.POST['content']
        page.save()
        
        # if the content was changed or the page is new, we need to create a new revision!
        if ((newpage == False) and (oldcontent != request.POST['content'])) or (newpage == True):
            revno = Revision.objects.filter(page=page).count() + 1
            
            newrev = Revision(page=page, revno=revno, content=request.POST['content'], author=request.user)
            newrev.save()
        
        #except:
        #    return render_to_response('error.html', {'error': "Es gab leider ein paar Probleme mit deinem Kommentar...",}, context_instance=RequestContext(request))
        if request.is_ajax():
            return render_to_response("wiki/page_content.html", {'object': page}, context_instance=RequestContext(request))
        else:
            return HttpResponseRedirect(page.get_absolute_url())
    
    else:
        if request.is_ajax():
            return render_to_response('wiki/edit.html', {'object': page,}, context_instance=RequestContext(request))
        else:
            return render_to_response('wiki/edit_page.html', {'object': page, 'newpage': newpage}, context_instance=RequestContext(request))


def revs(request, name, **kwargs):
    """list all revsions of a single page. todo: doc"""
    wikipage = get_object_or_404(Page, name=name)
    
    if (wikipage.status != 'public') and (not request.user.is_authenticated()):
        return render_to_response('error.html', {'error': "You are not allowed to view this page!",}, context_instance=RequestContext(request))
    
    revs = Revision.objects.filter(page=wikipage).order_by('-created')
    
    return object_list(request, revs, **kwargs)
    
def onerev(request, name, revno):
    """displays one rev of a wikipage. todo: doc"""
    wikipage = get_object_or_404(Page, name=name)
    
    if (wikipage.status != 'public') and (not request.user.is_authenticated()):
        return render_to_response('error.html', {'error': "You are not allowed to view this page!",}, context_instance=RequestContext(request))
    
    rev = get_object_or_404(Revision, page=wikipage, revno=revno)
    return render_to_response('wiki/rev.html', {'page': wikipage, 'rev': rev}, context_instance=RequestContext(request))
