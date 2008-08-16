from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from conescy.apps.everything.models import Entry

class EntryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    fieldsets = (
        (_('Content'), {'fields': ('title', 'content', 'tags',) }),
        (_('Meta'), {'fields': ('status', 'created', 'author', 'app',) }),
        (_('Extra'), {'classes': ('collapse',), 'fields': ('meta', 'slug',) }),
        # todo: display changed field!
    )
    radio_fields = {"status": admin.HORIZONTAL}
    
    list_display = ('title', 'app', 'author', 'created', 'status')
    list_display_links = ('title',)
    list_filter = ('status', 'app', 'created')
    search_fields = ['title', 'tags', 'content']

admin.site.register(Entry, EntryAdmin)