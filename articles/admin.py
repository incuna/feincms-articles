from django.contrib import admin
from django import forms
from incunafein.admin import editor
from models import DJANGOCAL_SYNC, Article, Category
from django.conf import settings

#class ArticleForm(forms.ModelForm):
#    category = forms.ModelChoiceField(queryset=Category.objects.filter(parent__isnull=False))

#    class Meta:
#        models = Article

class ArticleAdmin(editor.ItemEditor, admin.ModelAdmin):
    date_hierarchy = 'publication_date'
    list_display = ('__unicode__', 'category', 'publication_date', 'publication_end_date',)
    list_filter = ( 'category',)
    search_fields = ('title', 'slug',)
    prepopulated_fields = {
        'slug': ('title',),
        }

    show_on_top = ('title', 'category', 'tags')
    raw_id_fields = []
    #form = ArticleForm
    

class CategoryAdmin(editor.TreeEditor):
    list_display = ('__unicode__', )
    list_filter = ('parent',)
    prepopulated_fields = {
        'slug': ('name',),
        }
    if DJANGOCAL_SYNC:
        fieldsets = (
            (None, {
                'fields': ('name', 'slug', 'parent', 'calendar_feed', )
            }),
        )
        
 
admin.site.register(Article, ArticleAdmin)
admin.site.register(Category, CategoryAdmin)

