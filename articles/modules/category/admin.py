from django.contrib import admin

from .models import Category, CategoryAdmin


admin.site.register(Category, CategoryAdmin)
