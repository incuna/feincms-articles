from django.conf.urls import patterns, url
from django.db import models
from django.utils.translation import ugettext_lazy as _
from feincms.content.application import models as app_models

from feincms import extensions


class Extension(extensions.Extension):

    def handle_model(self):
        self.model.add_to_class('category', models.ForeignKey('articles.Category', verbose_name=_('category')))
        self.model._meta.unique_together += [('category', 'slug')]
        self.model.get_urlpatterns_orig = self.model.get_urlpatterns

        @classmethod
        def get_urlpatterns(cls):
            from articles.modules.category import views
            return patterns('',
                    url(r'^(?P<category_url>[a-z0-9_/-]+/)articles/(?P<slug>[a-z0-9_-]+)/$', views.CategoryArticleDetail.as_view(), name="article_detail"),
                    url(r'^(?P<category_url>[a-z0-9_/-]+/)articles/$', views.CategoryArticleList.as_view(), name='article_category'),
                    url(r'^$', views.CategoryArticleList.as_view(), name='article_index'),
            )
        self.model.get_urlpatterns = get_urlpatterns

        def get_absolute_url(self):
            return ('article_detail', 'articles.urls', (), {
                    'category_url': self.category.local_url,
                    'slug': self.slug,
                    })
        self.model.get_absolute_url = app_models.permalink(get_absolute_url)

    def handle_modeladmin(self, modeladmin):
        modeladmin.list_filter += ['category', ]
        modeladmin.list_display.insert(1, 'category', )
        modeladmin.add_extension_options(_('Category'), {
            'fields': ('category',),
        })
