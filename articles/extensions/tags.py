from django.conf.urls.defaults import patterns, url
from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import ugettext_lazy as _

try:
    from taggit.managers import TaggableManager
except ImportError:
   raise ImproperlyConfigured('You need to install django-taggit to use the tags extension')

def register(cls, admin_cls):
    cls.add_to_class('tags', TaggableManager(verbose_name=_('tags'), blank=True))

    cls.urlpatterns += patterns('taggit.views',
                                url(r'^tags/(?P<slug>[^/]+)/$', 'tagged_object_list', {'queryset': cls.objects.active}, name="article_tagged_list"),
                               )

    if admin_cls:
        if admin_cls.fieldsets:
            admin_cls.fieldsets[0][1]['fields'].append('tags')

