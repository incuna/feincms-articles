import warnings

from django.contrib.gis import admin
from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _
from feincms import extensions


class Extension(extensions.Extension):
    def handle_model(self):
        self.model.add_to_class(
            'location',
            models.PointField(verbose_name=_('location'), null=True, blank=True))

        from articles.models import ArticleManager

        class GeoArticleManager(ArticleManager, models.GeoManager):
            pass

        self.model.add_to_class('objects', GeoArticleManager())

    def handle_modeladmin(self, modeladmin):
        if not issubclass(modeladmin, admin.OSMGeoAdmin):
            warnings.warn(
                "The admin class articles ArticleAdmin class is not a sub class of django.contrib.gis.admin.OSMGeoAdmin. "
                "Consider setting ARTICLE_MODELADMIN_CLASS = 'django.contrib.gis.admin.OSMGeoAdmin'")

        modeladmin.add_extension_options(_('Location'), {
            'fields': ('location',),
            'classes': ('collapse',),
        })
