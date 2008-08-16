from django.utils.translation import ugettext_lazy as _
from django.db import models

class Day(models.Model):
    """A day full of stats! This model has a date field and a text field which contains a very cool dict with your stats!"""
    date = models.DateField(_("Date"), unique=True)
    stats = models.TextField(_("Stats"), help_text=_("Stats of the day, stored in a python dictionary"))
    
    class Meta:
        verbose_name = _("Day")
        verbose_name_plural = _("Days")
        get_latest_by = "date"
        ordering = ['-date']
    
    @models.permalink
    def get_absolute_url(self):
        return ('stats-day', [str(self.date)])
    
    def the_stats(self):
        """evalute the stats field"""
        return eval(self.stats)
    
    def __unicode__(self):
        return _("Daily Stats %(date)s") % {'date': str(self.date)}
