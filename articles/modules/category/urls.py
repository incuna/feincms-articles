from django.conf.urls import patterns, url


urlpatterns = patterns('articles.modules.category.views',
    url(r'^(?P<category_url>[a-z0-9_/-]+/)(?P<article>[a-z0-9_-]+).html$', 'article_detail', name="article_detail"),
    url(r'^(?P<category_url>[a-z0-9_/-]+/)$', 'article_category', name='article_category'),
    url(r'^$', 'article_category', name='article_index'),
)


