from django.conf import settings
from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import get_callable
from django.core.exceptions import ImproperlyConfigured
from django.conf.urls.defaults import patterns, url#, include

from feincms.admin import editor
from feincms.models import Base
from feincms.utils.managers import ActiveAwareContentManagerMixin

from incuna.db.models import AutoSlugField

import views


class ArticleManager(ActiveAwareContentManagerMixin, models.Manager):

    # A list of filters which are used to determine whether a page is active or not.
    # Extended for example in the datepublisher extension (date-based publishing and
    # un-publishing of pages)
    active_filters = [Q(active=True),]


class Article(Base):
    active = models.BooleanField(_('active'), default=True)

    title = models.CharField(max_length=255)
    slug = AutoSlugField(max_length=255, populate_from="title", help_text='This will be automatically generated from the name', unique=True, editable=True)

    summary = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['title', ]
        unique_together = []

    objects = ArticleManager()

    urlpatterns = patterns('',
        url(r'^$', views.ArticleList, name='article_index'),
        url(r'^(?P<article>[a-z0-9_-]+)/$', views.ArticleDetail, name='article_detail'),
    )

    @classmethod
    def remove_field(cls, f_name):
        # Removes the field form local fields list
        cls._meta.local_fields = [f for f in cls._meta.local_fields if f.name != f_name]

        # Removes the field setter if exists
        if hasattr(cls, f_name):
            delattr(cls, f_name)

    @classmethod
    def register_extension(cls, register_fn):
        register_fn(cls, ArticleAdmin)

    @classmethod
    def get_urls(cls):
        return cls.urlpatterns

    def __unicode__(self):
        return u"%s" % (self.title)

    @models.permalink
    def get_absolute_url(self):
        return ('article_detail', (), { 'article': self.slug, })

    @property
    def is_active(self):
        return Article.objects.active().filter(pk=self.pk).count() > 0


ModelAdmin = get_callable(getattr(settings, 'ARTICLE_MODELADMIN_CLASS', 'django.contrib.admin.ModelAdmin'))


class ArticleAdmin(editor.ItemEditor, ModelAdmin):
    list_display = ['__unicode__', 'active',]
    list_filter = []
    search_fields = ['title', 'slug', 'summary']
    filter_horizontal = []
    prepopulated_fields = {
        'slug': ('title',),
    }
    fieldsets = [
        (None, {
            'fields': ['active', 'title', 'slug', 'summary', ]
        }),
    ]
