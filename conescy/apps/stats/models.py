from django.db import models

class Day(models.Model):
    """A day full of stats! This model has a date field and a text field which contains a very cool dict with your stats!"""
    date = models.DateField("Date", unique=True)
    stats = models.TextField("Stats", help_text="Stats of the day, stored in a python dictionary")
    
    class Meta:
        verbose_name = "Day"
        verbose_name_plural = "Days"
        get_latest_by = "date"
        ordering = ['-date']
    
    @models.permalink
    def get_absolute_url(self):
        return ('stats-day', [str(self.date)])
    
    def the_stats(self):
        """evalute the stats field"""
        return eval(self.stats)
    
    def __unicode__(self):
        return "Daily Stats %s" % str(self.date)
