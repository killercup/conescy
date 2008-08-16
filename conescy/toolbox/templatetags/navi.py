from django import template
register = template.Library()

@register.simple_tag
def active_page(request, pattern, activeclass):
    """This is a useful tag for adding a class for the current page to your navigation.
    
    Example of usage::
        
        <li{% active_page request "^/(?P<project>.*)/overview/" " class='current'" %}>...</li>
    """
    import re
    if re.search(pattern, request.path):
        return activeclass
    return ''
