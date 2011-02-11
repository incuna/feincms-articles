from django.conf import settings
from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import get_callable
from django.core.exceptions import ImproperlyConfigured
from django.conf.urls.defaults import patterns, url#, include
from incuna.db.models import AutoSlugField
from incunafein.admin import editor
from feincms.models import Base

ModelAdmin = get_callable(getattr(settings, 'ARTICLE_MODELADMIN_CLASS', 'django.contrib.admin.ModelAdmin'))

class ArticleManager(models.Manager):

    # A list of filters which are used to determine whether a page is active or not.
    # Extended for example in the datepublisher extension (date-based publishing and
    # un-publishing of pages)
    active_filters = [Q(active=True),]

    @classmethod
    def apply_active_filters(cls, queryset, user=None):
        for filt in cls.active_filters:
            if callable(filt):
                queryset = filt(queryset, user)
            else:
                queryset = queryset.filter(filt)

        return queryset

    def active(self, user=None):
        return self.apply_active_filters(self, user=user)


class Article(Base):
    active = models.BooleanField(_('active'), default=True)

    title = models.CharField(max_length=255)
    slug = AutoSlugField(max_length=255, populate_from="title", help_text='This will be automatically generated from the name', unique=True, editable=True)


    summary = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['title', ]
        unique_together = []

    objects = ArticleManager()

    urlpatterns = patterns('articles.views',
                           url(r'^(?P<article>[a-z0-9_-]+).html$', 'article_detail', name="article_detail"),
                           url(r'^$', 'article_list', name='article_index'),
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
    def register_extensions(cls, *extensions):
        if not hasattr(cls, '_article_extensions'):
            cls._article_extensions = set()

        here = cls.__module__.split('.')[:-1]
        here_path = '.'.join(here + ['extensions'])

        for ext in extensions:
            if ext in cls._article_extensions:
                continue

            try:
                if isinstance(ext, basestring):
                    try:
                        fn = get_callable(ext + '.register', False)
                    except ImportError:
                        fn = get_callable('%s.%s.register' % ( here_path, ext ), False)
                # Not a string, so take our chances and just try to access "register"
                else:
                    fn = ext.register

                cls.register_extension(fn)
                cls._article_extensions.add(ext)
            except Exception, e:
                raise ImproperlyConfigured("%s.register_extensions('%s') raised an exception - '%s'" %
                                            (cls.__name__, ext, e))


    @classmethod
    def get_urls(cls):
        #final_urls = patterns()
        #for urlpattern in cls.urlpatterns:
        #    if callable(urlpattern):
        #        final_urls += urlpattern()
        #    else:
        #        final_urls += urlpattern

        #return final_urls
        return cls.urlpatterns

    def __unicode__(self):
        return u"%s" % (self.title)

    @models.permalink
    def get_absolute_url(self):
        return ('article_detail', (), { 'article': self.slug, })

    @property
    def is_active(self):
        return Article.objects.active().filter(pk=self.pk).count() > 0


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

