from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from django.conf.urls.defaults import patterns, url

def register(cls, admin_cls):
    cls.add_to_class('category', models.ForeignKey('articles.Category', verbose_name=_('category')))

    cls._meta.unique_together += [('category', 'slug')]

    @classmethod
    def get_urlpatterns(cls):
        return patterns('articles.modules.category.views',
                url(r'^(?P<category_url>[a-z0-9_/-]+/)(?P<slug>[a-z0-9_-]+)/$', 'article_detail', name="article_detail"),
                url(r'^(?P<category_url>[a-z0-9_/-]+/)$', 'article_category', name='article_category'),
                url(r'^$', 'article_category', name='article_index'),
       ) 
    cls.get_urlpatterns = get_urlpatterns
        

    def get_absolute_url(self):
        return ('article_detail', (), {
                'category_url': self.category.local_url,
                'slug': self.slug,
                })
    cls.get_absolute_url = models.permalink(get_absolute_url)

    # TODO: What happened to active_filters??
    #def active_filter(queryset, user=None):
    #    if user is not None and user.is_authenticated():
    #        queryset = queryset.filter(Q(category__access_groups__isnull=True) | Q(category__access_groups__in=user.groups.all()))
    #    else:
    #        queryset = queryset.filter(category__access_groups__isnull=True)

    #    return queryset

    #cls.objects.active_filters.append(active_filter)

    if admin_cls:
        admin_cls.list_filter += [ 'category',]
        admin_cls.list_display.insert(1, 'category', )


        if admin_cls.fieldsets:
            fields = admin_cls.fieldsets[0][1]['fields']
            try:
                at = fields.index('title')
            except ValueError:
                at = len(fields)
            fields.insert(at, 'category')

