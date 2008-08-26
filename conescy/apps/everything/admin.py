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
    
    def add_view(self, request,  *args, **kwargs):
        self._request = request
        return super(EntryAdmin, self).add_view(request,  *args, **kwargs)
    
    def change_view(self, request, *args, **kwargs):
        self._request = request
        return super(EntryAdmin, self).change_view(request,  *args, **kwargs)
    
    def formfield_for_dbfield(self, db_field, **kwargs):
        """Special thanks to Martin Mahner for providing the idea!
        see: http://www.mahner.org/weblog/spass-mit-newforms-admin-automatische-felder/
        """
        field = super(EntryAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        
        # Preselect current user as author
        if db_field.name == "author":
            field.initial = self._request.user.pk
        return field
    


admin.site.register(Entry, EntryAdmin)