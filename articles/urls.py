from django.conf import settings
from django.conf.urls.defaults import *

urlpatterns = patterns('articles.views',
    url(r'^(?P<article>[a-z0-9_-]+).html$', 'article_detail', name="article_detail"),
    url(r'^$', 'article_list', name='article_index'),
)

