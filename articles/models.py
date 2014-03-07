from django.conf import settings
from django.core.urlresolvers import get_callable

try:
    from feincms.admin.item_editor import ItemEditor
except ImportError:
    from feincms.admin.editor import ItemEditor

from feincms.extensions import ExtensionModelAdmin

from articles.bases import BaseArticle


class Article(BaseArticle):
    pass


ModelAdmin = get_callable(getattr(settings, 'ARTICLE_MODELADMIN_CLASS', 'django.contrib.admin.ModelAdmin'))


class ArticleAdmin(ItemEditor, ExtensionModelAdmin):
    list_display = ['title', 'active',]
    list_filter = []
    search_fields = ['title', 'slug']
    filter_horizontal = []
    prepopulated_fields = {
        'slug': ('title',),
    }
    fieldsets = [
        (None, {
            'fields': ['active', 'title', 'slug']
        }),
        # <-- insertion point, extensions appear here, see insertion_index above
    ]

    fieldset_insertion_index = 1

