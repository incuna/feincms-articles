from django.conf import settings
from django.conf.urls.defaults import *
from models import Article#, Category

urlpatterns = patterns(
    'tagging.views',
    url(r'^tag/(?P<tag>[^/]+)/$', 'tagged_object_list', 
        dict(queryset_or_model=Article, 
             #paginate_by=10, 
             allow_empty=True,
             #template_object_name='articles',
             template_name='articles/article_list.html',
             extra_context={'category': None},
            ),
        name="article_tag"),
                      )

urlpatterns += patterns('articles.views',
    url(r'^(?P<category_url>[a-z0-9_/-]+/)(?P<slug>[a-z0-9_-]+).html$', 'article_detail', name="article_detail"),
    url(r'^(?P<category_url>[a-z0-9_/-]+/)$', 'article_category', name='article_category'),
    url(r'^$', 'article_category', name='article_index'),
    
) 

