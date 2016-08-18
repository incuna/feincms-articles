from django.contrib import admin

from .bases import ArticleAdmin
from .models import Article


try:
    admin.site.unregister(Article)
except admin.sites.NotRegistered:
    pass
admin.site.register(Article, ArticleAdmin)
