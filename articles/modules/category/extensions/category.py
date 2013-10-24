from django.conf.urls.defaults import patterns, url
from django.db import models
from django.utils.translation import ugettext_lazy as _
from feincms.content.application import models as app_models


def register(cls, admin_cls):
    cls.add_to_class('category', models.ForeignKey('articles.Category', verbose_name=_('category')))

    cls._meta.unique_together += [('category', 'slug')]

    @classmethod
    def get_urlpatterns(cls):
        from articles.modules.category import views
        return patterns('',
                url(r'^(?P<category_url>[a-z0-9_/-]+/)articles/(?P<slug>[a-z0-9_-]+)/$', views.CategoryArticleDetail.as_view(), name="article_detail"),
                url(r'^(?P<category_url>[a-z0-9_/-]+/)articles/$', views.CategoryArticleList.as_view(), name='article_category'),
                url(r'^$', views.CategoryArticleList.as_view(), name='article_index'),
       )
    cls.get_urlpatterns = get_urlpatterns

    def get_absolute_url(self):
        return ('article_detail', 'articles.urls', (), {
                'category_url': self.category.local_url,
                'slug': self.slug,
                })
    cls.get_absolute_url = app_models.permalink(get_absolute_url)

    if admin_cls:
        admin_cls.list_filter += [ 'category',]
        admin_cls.list_display.insert(1, 'category', )
        admin_cls.add_extension_options(_('Category'), {
            'fields': ('category',),
        })
