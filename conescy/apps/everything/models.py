import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from tagging.fields import TagField

class Entry(models.Model):
    """A model for as many uses as possible. Only consits of a title, content and tag field and some meta fields like date and author. Additionally it has a text-meta field which can contain any other meta datas, e.g. Python dictionaries or XML data."""
    title = models.CharField(_("Title"), max_length=200)
    content = models.TextField(_("Content"))
    tags = TagField()
    
    created = models.DateTimeField(_("Created"), default=datetime.datetime.now)
    changed = models.DateTimeField(_("Changed"), auto_now=True)
    author = models.ForeignKey(User, verbose_name=_("Author"))
    
    meta = models.TextField(_("Metadata"), blank=True)
    STATUS_CHOICES = (
        ('public', _('Public')),
        ('private', _('Private')),
        ('draft', _('Draft')),
    )	
    status = models.CharField(_("Status"), max_length=16, choices=STATUS_CHOICES)
    slug = models.SlugField(_("Slug"), unique=True, db_index=True)
    
    app = models.CharField(_("Instance"), max_length=32)
    
    class Meta:
        verbose_name = _("Entry")
        verbose_name_plural = _("Entries")
        get_latest_by = "created"
        ordering = ['-created']
    
    @models.permalink
    def get_absolute_url(self):
        try:
            return ("%s-detail" % self.app, [self.slug])
        except:
            return ""
    
    def get_meta_yaml(self):
        import yaml
        return yaml.load(self.meta)
    
    def get_meta(self):
        return eval(self.meta)
    
    def get_author_name(self):
        return self.author
    
    def get_the_content(self):
        return self.content
    
    def get_creation_date(self):
        return self.created
    
    def get_the_title(self):
        return self.title
    
    def __unicode__(self):
        return "%s in %s" % (self.title, self.app)
