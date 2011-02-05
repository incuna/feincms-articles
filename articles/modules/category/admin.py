from django.contrib import admin
from incunafein.admin import editor
from incuna.db.models import AutoSlugField
from models import Category

class CategoryAdmin(editor.TreeEditor):
    list_display = ('__unicode__', 'order_by', )
    list_filter = ('parent',)
    prepopulated_fields = {
        'slug': ('name',),
        }
    #if DJANGOCAL_SYNC:
    #    fieldsets = (
    #        (None, {
    #            'fields': ('name', 'slug', 'parent', 'calendar_id', 'order_by')
    #        }),
    #        ('Permissions', {
    #            'classes': ('collapse',),
    #            'fields': ('access_groups',)
    #        }),
    #    )
 
admin.site.register(Category, CategoryAdmin)


