import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from tagging.fields import TagField

class Page(models.Model):
    """A simple wiki page. todo: doc"""
    name = models.CharField(_("Name"), max_length=100, unique=True, db_index=True)
    content = models.TextField(_("Content"))
    tags = TagField()
    
    created = models.DateTimeField(_("Created"), default=datetime.datetime.now)
    changed = models.DateTimeField(_("Changed"), auto_now=True)
    STATUS_CHOICES = (
        ('public', _('Public')),
        ('private', _('Private')),
        ('draft', _('Draft')),
    )    
    status = models.CharField(_("Status"), max_length=16, choices=STATUS_CHOICES)
    
    class Meta:
        verbose_name = _("Page")
        verbose_name_plural = _("Pages")
        get_latest_by = "created"
        ordering = ['-created']
    
    @models.permalink
    def get_absolute_url(self):
        return ('wiki-page', [self.name])
    
    def __unicode__(self):
        return self.name
    
    def get_author_name(self):
        """uhh.. a wiki page doesn't have an author!"""
        return ""    
    
    def get_creation_date(self):
        return self.created
    
    def get_the_content(self):
        return self.content
    
    def get_the_title(self):
        return self.name


class Revision(models.Model):
    """A revsion of a wiki page. todo: doc"""
    page = models.ForeignKey(Page, verbose_name=_("Page"))
    revno = models.IntegerField(_("Revision Number"))
    
    content = models.TextField(_("Content"))
    
    author = models.ForeignKey(User, verbose_name=_("Author"))
    created = models.DateTimeField(_("Created"), default=datetime.datetime.now)
    
    class Meta:
        verbose_name = _("Revision")
        verbose_name_plural = _("Revisions")
        get_latest_by = "created"
        ordering = ['-created']
        
    @models.permalink
    def get_absolute_url(self):
        return ('wiki-revision', [self.page, self.revno])
    
    def __unicode__(self):
        return _('Revision %(revno)s of "%(page)s"') % {'revno': str(self.revno), 'page': self.page}
    
    def get_author_name(self):
        return self.author
    
    def get_the_content(self):
        return self.content
    
    def get_the_title(self):
        return self.__unicode__
    
    def get_creation_date(self):
        return self.created
