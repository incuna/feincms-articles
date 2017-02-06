from django.conf import settings
from django.core.urlresolvers import get_callable, reverse_lazy
from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from django.conf.urls import url
from django.utils.encoding import python_2_unicode_compatible

try:
    from feincms.admin.item_editor import ItemEditor
except ImportError:
    from feincm.admin.editor import ItemEditor
from feincms.content.application import models as app_models
from feincms.models import Base
from feincms.module.mixins import ContentModelMixin
from feincms.utils.managers import ActiveAwareContentManagerMixin


class ArticleManager(ActiveAwareContentManagerMixin, models.Manager):
    active_filters = {'simple-active': Q(active=True)}


@python_2_unicode_compatible
class BaseArticle(ContentModelMixin, Base):
    active = models.BooleanField(_('active'), default=True)

    title = models.CharField(_('title'), max_length=255)
    slug = models.SlugField(
        _('slug'),
        max_length=255,
        help_text=_('This will be automatically generated from the name'),
        unique=True,
        editable=True,
    )

    class Meta:
        ordering = ['title']
        unique_together = []
        verbose_name = _('article')
        verbose_name_plural = _('articles')
        abstract = True

    objects = ArticleManager()

    @classmethod
    def get_urlpatterns(cls):
        from . import views
        return [
            url(r'^$', views.ArticleList.as_view(), name='article_index'),
            url(r'^(?P<slug>[a-z0-9_-]+)/$', views.ArticleDetail.as_view(), name='article_detail'),
        ]

    @classmethod
    def remove_field(cls, f_name):
        """Remove a field. Effectively inverse of contribute_to_class"""
        # Removes the field form local fields list
        cls._meta.local_fields = [f for f in cls._meta.local_fields if f.name != f_name]

        # Removes the field setter if exists
        if hasattr(cls, f_name):
            delattr(cls, f_name)

    @classmethod
    def get_urls(cls):
        return cls.get_urlpatterns()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse_lazy('article_detail', kwargs={'slug': self.slug})

    @property
    def is_active(self):
        return self.__class__.objects.active().filter(pk=self.pk).count() > 0


ExtensionModelAdmin = get_callable(getattr(
    settings, 'ARTICLE_MODELADMIN_CLASS', 'feincms.extensions.ExtensionModelAdmin'))


class ArticleAdmin(ItemEditor, ExtensionModelAdmin):
    list_display = ['title', 'active']
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
