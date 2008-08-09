from django import template
from conescy.apps.comments.models import Comment
register = template.Library()

@register.inclusion_tag('comments/form.html')    
def display_comments(request, ref_app, ref_id):
    """Display comments and comment form for a specific object.

**Please make sure that you have added the** `request`_ **context-preprocessor installed and active for all the templates you want to use this template tag in! Without it, the first argument for this function is empty and you wont get all the infomation you need!**

.. _request: http://www.djangoproject.com/documentation/templates_python/#django-core-context-processors-request

Usage::

    {% display_comments request 'YOUR_APP_USED'.'YOUR_CURRENT_MODEL' 'YOUR_OBJECT_ID' %}

So in your Conescy blog template you insert e.g.::

    {% display_comments request "blog.Entry." Entry.id %}

(where ``Entry.id`` is a variable for the ID of your current entry)

It should work with most django apps and offers an easy method to add commenting!"""
    
    cookies = {'name': request.COOKIES.get('comments_name', ''), 'mail': request.COOKIES.get('comments_mail', ''), 'url': request.COOKIES.get('comments_url', '')}
    ref = ref_app + str(ref_id)
    comments = Comment.objects.filter(ref=ref, status='ok').order_by('date')
    return {'comments': comments, 'ref': ref, 'ref_app': ref_app, 'ref_id': ref_id, 'user': request.user, 'cookies': cookies}

@register.simple_tag
def comments_count(ref_app, ref_id):
    """ Returns the number of comments for a single entry.

Usage::

    {% comments_count 'YOUR_APP_USED'.'YOUR_CURRENT_MODEL' 'YOUR_OBJECT_ID' %}

Useful for blog startpages in combination with display_comments!"""
    
    ref = ref_app + str(ref_id)
    ccount = Comment.objects.filter(ref=ref, status='ok').count()
    return ccount
