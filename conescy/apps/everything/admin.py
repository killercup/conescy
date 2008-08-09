from django.contrib import admin
from conescy.apps.everything.models import Entry

class EntryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    fieldsets = (
        ('Inhalt', {'fields': ('title', 'content', 'tags',) }),
        ('Meta', {'fields': ('status', 'created', 'author', 'app',) }),
        ('Extra', {'classes': ('collapse',), 'fields': ('meta', 'slug',) }),
        # todo: display changed field!
    )
    
    list_display = ('title', 'app', 'author', 'created', 'status')
    list_display_links = ('title',)
    list_filter = ('status', 'app', 'created')
    search_fields = ['title', 'tags', 'content']

admin.site.register(Entry, EntryAdmin)