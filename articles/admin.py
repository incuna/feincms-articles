from django.contrib import admin
from django import forms
from feincms.admin import editor
from models import Article, Category
 
#class ArticleForm(forms.ModelForm):
#    category = forms.ModelChoiceField(queryset=Category.objects.filter(parent__isnull=False))

#    class Meta:
#        models = Article

class ArticleAdmin(editor.ItemEditor, admin.ModelAdmin):
    date_hierarchy = 'publication_date'
    list_display = ('__unicode__', 'publication_date', 'publication_end_date',)
    list_filter = ( 'category',)
    search_fields = ('title', 'slug',)
    prepopulated_fields = {
        'slug': ('title',),
        }

    show_on_top = ('title', 'category', 'tags')
    raw_id_fields = []
    #form = ArticleForm
    

class CategoryAdmin(editor.TreeEditor):
    list_display = ('name', 'slug')
    list_filter = ('parent',)
    prepopulated_fields = {
        'slug': ('name',),
        }
 

admin.site.register(Article, ArticleAdmin)
admin.site.register(Category, CategoryAdmin)

