from django.contrib import admin
from django import forms
from incunafein.admin import editor
from models import DJANGOCAL_SYNC, Article, Category
from django.conf import settings

class ArticleAdmin(editor.ItemEditor, admin.ModelAdmin):
    date_hierarchy = 'publication_date'
    list_display = ('__unicode__', 'category', 'publication_date', 'publication_end_date',)
    list_filter = ( 'category',)
    search_fields = ('title', 'slug',)
    prepopulated_fields = {
        'slug': ('title',),
        }

    filter_horizontal = ('access_groups',)
    fieldsets = [
        (None, {
            'fields': ('title', 'slug', 'category', 'tags', 'summary', 'publication_date', 'publication_end_date', 'thumbnail' )
        }),
        ('Permissions', {
            'classes': ('collapse',),
            'fields': ('access_groups',)
        }),
    ]

class CategoryAdmin(editor.TreeEditor):
    list_display = ('__unicode__', 'order_by', )
    list_filter = ('parent',)
    prepopulated_fields = {
        'slug': ('name',),
        }
    if DJANGOCAL_SYNC:
        fieldsets = (
            (None, {
                'fields': ('name', 'slug', 'parent', 'calendar_id', 'order_by')
            }),
        )
 
admin.site.register(Article, ArticleAdmin)
admin.site.register(Category, CategoryAdmin)

