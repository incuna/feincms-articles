from django.contrib import admin

from .bases import ArticleAdmin
from .models import Article


admin.site.register(Article, ArticleAdmin)
