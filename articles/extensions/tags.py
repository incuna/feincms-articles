from django.utils.translation import ugettext_lazy as _
from django.conf.urls.defaults import patterns, url
#from tagging.fields import TagField
from taggit.managers import TaggableManager

def register(cls, admin_cls):
    #cls.add_to_class('tags', TagField(_('tags'), null=True, blank=True))

    cls.add_to_class('tags', TaggableManager())

    cls.urlpatterns += patterns('taggit.views',
                                url(r'^tags/(?P<slug>[a-z0-9_-]+)/$', 'tagged_object_list', {'queryset': cls.objects.active()}, name="article_tagged_list"),
                               )

    if admin_cls:
        if admin_cls.fieldsets:
            admin_cls.fieldsets[0][1]['fields'].append('tags')

