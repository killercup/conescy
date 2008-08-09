from django import template
from tagging.models import Tag, TaggedItem
from tagging.utils import calculate_cloud
from conescy.apps.everything.models import Entry

register = template.Library()

@register.inclusion_tag('tags/tagcloud.html')
def everytagcloud(app, steps=5, min_count=None):
    """
    Includes a cool tag cloud based on some everything entries!
    
    Usage::
    
        {% load everythingtags %}
        
        {% everytagcloud blog 5 2 %}
    
    This includes a cloud of blog-tags which increase font-size in 5 steps 
    (you need to add some CSS) and have a minimum count of two.
    
    The number of steps is 5 by default, min_count is optional.
    """
    instance = Entry.objects.filter(app=app, status="public")
    #tags = Tag.objects.cloud_for_model(instance, steps=steps, min_count=min_count)
    taglist = list(Tag.objects.usage_for_queryset(instance, counts=True, min_count=min_count))
    tags = calculate_cloud(taglist, steps=steps)
    return {'tags': tags}


class GetEverythingObjects(template.Node):
    def __init__(self, app, count):
        self.app = app
        self.count = int(count)

    def render(self, context):
        entries = Entry.objects.filter(app=self.app, status="public").order_by("-created")[:self.count]
        context[str(self.app)+'_list'] = entries
        return ''

def do_get_everything_objects(parser, token):
    """
    Includes some objects of an everything instance.
    
    Usage::
    
        {% load everythingtags %}
        
        {% get_everything blog 5 %}
        
        {% for object in blog_list %}
            <li><a href="{{ object.get_absolute_url }}/" title="{{object.title}}">{{object.title}}</a></li>
        {% endfor %}
    
    After loading the template tag, the tag ``{% get_everything blog 5 %}`` gets five latest objects from 
    everything with the app (instance) "blog" and, of course, the status "public". The objects are now
    available in a list/queryset called ``<APP>_list``, e.g. ``blog_list`` if you queried the app "blog".
    The last three lines are an example how to include the objects into your template.
    """
    bits = token.contents.split()
    if len(bits) is not 3:
        raise template.TemplateSyntaxError("%s requires exactly two arguments!" % bits[0])
    return GetEverythingObjects(bits[1], bits[2])

register.tag('get_everything', do_get_everything_objects)
