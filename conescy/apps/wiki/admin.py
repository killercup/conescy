from django.contrib import admin
from conescy.apps.wiki.models import Page, Revision

class PageAdmin(admin.ModelAdmin):
    radio_fields = {"status": admin.HORIZONTAL}
    
    list_display = ('name', 'created')
    list_display_links = ('name',)
    search_fields = ('name', 'content', 'tags')
    list_filter = ('created',)


class RevisionAdmin(admin.ModelAdmin):
    list_display = ('page', 'revno', 'author', 'created')
    list_display_links = ('page',)
    search_fields = ('content', 'revno', 'page')
    list_filter = ('created', 'author')

admin.site.register(Page, PageAdmin)
admin.site.register(Revision, RevisionAdmin)