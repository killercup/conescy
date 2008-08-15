import datetime
from django.db import models
from django.contrib.auth.models import User
from tagging.fields import TagField

class Page(models.Model):
    """A simple wiki page. todo: doc"""
    name = models.CharField("Name", max_length=100, unique=True, db_index=True)
    content = models.TextField("Content")
    tags = TagField()
    
    created = models.DateTimeField("Created", default=datetime.datetime.now)
    changed = models.DateTimeField("Changed", auto_now=True)
    STATUS_CHOICES = (
        ('public', 'Public'),
        ('private', 'Private'),
        ('draft', 'Draft'),
    )    
    status = models.CharField(max_length=16, choices=STATUS_CHOICES)
    
    class Meta:
        verbose_name = "Page"
        verbose_name_plural = "Pages"
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
    page = models.ForeignKey(Page)
    revno = models.IntegerField("Revsion Number")
    
    content = models.TextField("Content")
    
    author = models.ForeignKey(User)
    created = models.DateTimeField("Created", default=datetime.datetime.now)
    
    class Meta:
        verbose_name = "Revision"
        verbose_name_plural = "Revisions"
        get_latest_by = "created"
        ordering = ['-created']
        
    @models.permalink
    def get_absolute_url(self):
        return ('wiki-revision', [self.page, self.revno])
    
    def __unicode__(self):
        return "Revision %s of %s" % (str(self.revno), self.page)
    
    def get_author_name(self):
        return self.author
    
    def get_the_content(self):
        return self.content
    
    def get_the_title(self):
        return self.__unicode__
    
    def get_creation_date(self):
        return self.created
