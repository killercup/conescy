import re
import string
import dateutil

try:
    from cStringIO import StringIO
except:
    from StringIO import StringIO
try:
    import cElementTree as ET
except:
    import ElementTree as ET

from django.utils.encoding import *

from conescy.apps.everything.models import *
from conescy.apps.comments.models import *

def wordpress(xml, instance, author):
    """Imports from an wordpress export xml file directly into everything.
    Uses cElementTree (http://effbot.org/zone/celementtree.htm) for XML access."""
    
    xml = ET.parse(StringIO(xml['content']))
    root = xml.getroot().find("channel")
    
    for i in root.findall("item"):
        slug = i.findtext("{http://wordpress.org/export/1.0/}post_name")
        # Check if this Entry already exists
        try:
            e = Entry.objects.get(slug=slug)
        except:
            # Create a new everything entry!
            tags = []
            try:
                for cat in i.findall("category"):
                    tags.append(cat.text)
                tagstring = string.join(tags, ", ")
            except:
                tagstring = ""
            
            if i.findtext("{http://wordpress.org/export/1.0/}status") == "publish":
                status = "public"
            else: status = "draft"
            date = dateutil.parser.parse(i.findtext("{http://wordpress.org/export/1.0/}post_date"))
            content = i.findtext("{http://purl.org/rss/1.0/modules/content/}encoded")
            
            e = Entry(
                title=i.findtext("title"),
                content=content,
                tags=tagstring,
                slug=slug,
                status=status,
                app=instance,
                author_id=int(author),
            )
            e.save()
            e.created = date
            e.save()
            # print "Imported Entry " + e.title
        
        # Import the comments, too!
        for c in i.findall("{http://wordpress.org/export/1.0/}comment"):
            ref = "%s.entry.%s" % (instance, e.id)
            
            content=c.find("{http://wordpress.org/export/1.0/}comment_content")
            content = ET.tostring(content)
            thecontent = content.replace('<ns0:comment_content xmlns:ns0="http://wordpress.org/export/1.0/">', '',).replace('</ns0:comment_content>', '')
            themail = c.findtext("{http://wordpress.org/export/1.0/}comment_author_email")
            
            # Check if this Comment does already exists
            try:
                v = Comment.objects.get(ref=ref, content=thecontent, mail=themail)
            except:
                if str(c.findtext("{http://wordpress.org/export/1.0/}comment_approved")) == str(1):
                    status = "ok"
                else:
                    status = "unsure"
                
                v = Comment(
                    name=c.findtext("{http://wordpress.org/export/1.0/}comment_author"),
                    mail=themail,
                    url=c.findtext("{http://wordpress.org/export/1.0/}comment_author_url"),
                    ip=c.findtext("{http://wordpress.org/export/1.0/}comment_author_IP"),
                    content=thecontent,
                    date=dateutil.parser.parse(c.findtext("{http://wordpress.org/export/1.0/}comment_date")),
                    status=status,
                    ref=ref,
                )
                v.save()
        
    

def rss(xml, instance, author):
    """Imports from RSS Feed into Everything!"""
    from django.template.defaultfilters import slugify
    xml = ET.parse(StringIO(xml['content']))
    root = xml.getroot().find("channel")
    
    for i in root.findall("item"):
        title = i.findtext("title")
        slug = slugify(title)
        try:
            e = Entry.objects.get(slug=slug)
        except:
            tags = []
            try:
                for cat in i.findall("category"):
                    tags.append(cat.text)
                tagstring = string.join(tags, ", ")
            except:
                tagstring = ""
            
            e = Entry(
                title=title,
                content=i.findtext("description"),
                tags=tagstring,
                slug=slug,
                status="public",
                app=instance,
                author_id=int(author),
            )
            e.save()
            e.created = dateutil.parser.parse(i.findtext("pubDate"))
            e.save()
            print "Imported Entry " + e.title
        
