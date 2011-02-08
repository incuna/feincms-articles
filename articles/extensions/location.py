import warnings
from django.contrib.gis.db import models
from django.contrib.gis import admin
from django.utils.translation import ugettext_lazy as _


def register(cls, admin_cls):
    cls.add_to_class('location', models.PointField(verbose_name=_('location'), null=True, blank=True))

    from articles.models import ArticleManager
    class GeoArticleManager(ArticleManager, models.GeoManager):
        pass
    cls.add_to_class('objects', GeoArticleManager())

    if admin_cls:
        if not issubclass(admin_cls, admin.OSMGeoAdmin):
            warnings.warn("The admin class articles ArticleAdmin class is not a sub class of django.contrib.gis.admin.OSMGeoAdmin. "
                          "Consider setting ARTICLE_MODELADMIN_CLASS = 'django.contrib.gis.admin.OSMGeoAdmin'")

        if admin_cls.fieldsets:
            admin_cls.fieldsets.append((_('Location'), {
                    'fields': ['location'],
                    'classes': ('collapse',),
                }))
