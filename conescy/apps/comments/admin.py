from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from conescy.apps.comments.models import Comment

class CommentAdmin(admin.ModelAdmin):    
    fieldsets = (
        (_('Author'), {'fields': ('username', ('name', 'mail', 'url')) }),
        (_('Content'), {'fields': ('content', 'status') }),
        (_('Meta'), {'classes': 'collapse','fields': ('date', 'ref', 'ip') }),
    )
    radio_fields = {"status": admin.HORIZONTAL}
    
    list_display = ('__unicode__', 'date', 'ref', 'status')
    search_fields = ['name', 'mail', 'username', 'url', 'content',]
    list_filter = ('date', 'status', 'ref')

admin.site.register(Comment, CommentAdmin)