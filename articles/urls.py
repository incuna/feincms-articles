from django.conf.urls.defaults import *
from articles.models import Article

#urlpatterns = patterns('articles.views',
#    url(r'^(?P<article>[a-z0-9_-]+).html$', 'article_detail', name="article_detail"),
#    url(r'^$', 'article_list', name='article_index'),
#)

urlpatterns = Article.get_urls()

print urlpatterns


