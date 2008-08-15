from django.contrib import admin
from conescy.apps.stats.models import Day

class DayAdmin(admin.ModelAdmin):
    list_display = ('__unicode__',)
    search_fields = ['date', 'stats']
    list_filter = ('date',)

admin.site.register(Day, DayAdmin)