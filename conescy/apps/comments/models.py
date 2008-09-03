import datetime
from django.utils.translation import ugettext_lazy as _
from django.db import models

class Comment(models.Model):
    """This a comment, you can virtually include it in any other Conescy app! Some things you should know:
    
     - We use the a simple charfield for the relation between the comment and the object. this field e.g. get the value 'blog.entry.15', so we can split this into the app, the model and the id. Easier than the contenttype-framework I think (and this can be expanded to use comment responses and stuff like that in furture).
    
     - A comment can either be made by a logged in user or by a normal visitor, who needs to enter his name, mail address and optionally a website url
    
     - The status will be set by the view function (captures spam, set comments to "deleted", etc.), see the views.py!
    """
    # comments can be made by a logged in user
    username = models.PositiveIntegerField(help_text=_("If the comment was made by a logged in user, this field contains his/her user id. Otherwise the name, mail and url fields below should be filled."), blank=True, null=True)
    
    # or by a visitor
    name = models.CharField(_("Name"), blank=True, max_length=100)
    mail = models.EmailField(_("Mail-Address"), blank=True)
    url = models.URLField(_("Website-URL"), blank=True, verify_exists=True)
    ip = models.IPAddressField(_("IP-Address"))
    
    # a comment has a text field for the comment itself
    content = models.TextField(_("Content"))
    
    # the date is quite important ;)
    date = models.DateTimeField(_("Created"), default=datetime.datetime.now)
    
    # here is our relationship the the object we are commenting
    # this will finally look like "blog.entry.15"
    ref = models.CharField(_("Reference"), max_length=50, db_index=True)
    
    # well, we all hate spam and abuse... let's do something against it!
    STATUS_CHOICES = (
        ('ok', _('Approved Comment')),
        ('unsure', _('Spam?')),
        ('spam', _('Spam!!')),
        #even if a comment is marked as removed, it is not removed! so you cant do anything wrong!
        #todo: write a function to delete deleted comments after a special time periode!
        ('deleted', _('Deleted'))
    )
    status = models.CharField(_("Status"), max_length=16, choices=STATUS_CHOICES)
    
    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")
        get_latest_by = "date"
        ordering = ['-date']
    
    def get_author_name(self):
        """return the username or the commenter's name"""
        if self.name != '':
            return self.name
        else:
            from django.contrib.auth.models import User
            u = User.objects.get(id=self.username)
            return u.username
    
    def get_author_url(self):
        # todo: this should interact with a profiles app to get the url of logged in users.
        return self.url
    
    def get_ref_object(self):
        """Returns the referenced object or None if the object does not exists."""
        try:
            refs = self.ref.split('.')
            try:
                exec("from conescy.apps.%s" % refs[0])
            except:
                refs[0] = "everything"
            exec("from conescy.apps.%s.models import %s as Model" % (refs[0], refs[1].capitalize()))
            ref_object = Model.objects.get(id=refs[2])
            return ref_object
        except:
            raise
    
    def get_absolute_url(self):
        """Get the absolute url for the comment based on the absolute url of the reference object!"""
        return self.get_ref_object().get_absolute_url()
    
    def get_the_title(self):
        """Display a nice 'title' for the comment, based on some meta information."""
        return _("Comment #%(commentid)s on '%(reference)s' by %(author)s") % {'commentid': str(self.id), 'reference': self.get_ref_object().title, 'author': self.get_author_name()}
    
    def get_creation_date(self):
        return self.date
    
    def get_the_content(self):
        return self.content
    
    def __unicode__(self):
        return _('Comment #%(commentid)s by %(author)s') % {'commentid': str(self.id), 'author': self.get_author_name()}
    
