from django.conf import settings
from django.conf.urls.defaults import *
from models import Article#, Category

urlpatterns = patterns('articles.views',
    url(r'^(?P<category_url>[a-z0-9_/-]+/)(?P<slug>[a-z0-9_-]+).html$', 'article_detail', name="article_detail"),
    url(r'^(?P<category_url>[a-z0-9_/-]+/)$', 'article_category', name='article_category'),
    url(r'^$', 'article_category', name='article_index'),
)

