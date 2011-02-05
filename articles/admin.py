from django.contrib import admin
from models import Article, ArticleAdmin

admin.site.register(Article, ArticleAdmin)

