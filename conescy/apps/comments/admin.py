from django.contrib import admin
from conescy.apps.comments.models import Comment

class CommentAdmin(admin.ModelAdmin):    
    fieldsets = (
        ('Author', {'fields': ('username', ('name', 'mail', 'url')) }),
        ('Content', {'fields': ('content', 'status') }),
        ('Reference', {'classes': 'collapse','fields': ('ref', 'ip') }),
        # todo: display date field!
    )
    radio_fields = {"status": admin.HORIZONTAL}
    
    list_display = ('__unicode__', 'date', 'ref', 'status')
    search_fields = ['name', 'mail', 'username', 'url', 'content',]
    list_filter = ('date', 'status', 'ref')

admin.site.register(Comment, CommentAdmin)