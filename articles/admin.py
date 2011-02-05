from django.contrib import admin
from models import DJANGOCAL_SYNC, Article, ArticleAdmin


admin.site.register(Article, ArticleAdmin)

