import datetime
from dateutil.parser import *

from django.http import *
from django.template import RequestContext
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.utils.translation import ugettext as _

from conescy.apps.comments.models import Comment
from conescy.apps.comments.forms import CommentForm

@require_POST
def save(request, **kwargs):
    """Check if the given comment is valid and then save it.
    
To make sure no spam comes in, I've renamed the fieldes:
    
- name = 'eins'
- mail = 'zwei'
- url = 'drei' 
    
and finally the spam check is called 'author'! ;)
    
Please note that a comment by a logged in user will only have the fields 'username' and 'content' (and 'date', 'ip' and 'ref') filled!
    """
    
    # first spam check. if the "author" field is filled, this is made by a spam bot!
    if request.POST['author'] != '':
        return render_to_response('error.html', {'error': "I got you, stupid spam bot!",}, context_instance=RequestContext(request))
    else:
        status = 'ok'
    
    if request.POST.get('username'):
        if request.user.is_authenticated():
            # this is a comment made by a logged in user!
            # create a new comment
            c = Comment(
                username=int(request.POST['username']),
                content=request.POST['content'],
            )
        else:
            # the "username" field is filled but the user is not logged in?! spam!
            return render_to_response('error.html', {'error': _("The 'username' field was filled, but you are not logged in!"),}, context_instance=RequestContext(request))
    else:
        # this comment was made by normal visitor -- for the stupid field names see above!
        # first check the date with the form and then use the cleaned data
        check = CommentForm({
            'name': request.POST['eins'], 
            'mail': request.POST['zwei'], 
            'url': request.POST['drei'],
            'content': request.POST['content'],
        })
        if check.is_valid():
            c = Comment(
                name=check.cleaned_data['name'],
                mail=check.cleaned_data['mail'],
                url=check.cleaned_data['url'],
                content=check.cleaned_data['content'],
            )
        else:
            # if the form is not valid, there must be an error somewhere
            return render_to_response('error.html', {'error': _("There was a problem with your comment, I'm sorry... :("),}, context_instance=RequestContext(request))
    
    # fill the other fields of our comment
    c.ip = request.META.get('REMOTE_ADDR', '')
    c.date = datetime.datetime.now()
    c.status = status
    c.ref = str(request.POST['ref'])
    c.save()
    
    if request.is_ajax():
        comments = Comment.objects.filter(id=c.id)
        template_commentslist = kwargs.get("template_name", False) or "comments/comments_list.html"
        response = render_to_response(template_commentslist, {'comments': comments, 'ajaxcomments': True}, context_instance=RequestContext(request))
    else:
        response = HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
    # set some cookies the remember this dear commenter! the cookies' max_age is 90 days
    response.set_cookie("comments_name", c.name, max_age=7776000)
    response.set_cookie("comments_mail", c.mail, max_age=7776000)
    response.set_cookie("comments_url", c.url, max_age=7776000)
    
    # go for it!
    return response


@login_required
def delete(request, comment):
    """Simply set the Comment to status 'deleted'. This function is only available to logged in users!
    Todo: Make this only accept POST for security!
    """
    c = get_object_or_404(Comment, id=comment)
    # not many people are allowed to delete a comment! (just the author and the superuser)
    if (request.user.id == c.username) or request.user.is_superuser:
        c.status = "deleted"
        c.save()
        if request.is_ajax():
            return HttpResponse("Deleted.")
        else:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return render_to_response('error.html', {'error': _("You are not allowed to delete that comment!"),}, context_instance=RequestContext(request))


