from haystack.indexes import *
from haystack import site
from models import Article

class ArticleIndex(SearchIndex):
    name = CharField(model_attr='title')
    text = CharField(document=True, use_template=True)

    def get_queryset(self):
        """Used when the entire index for model is updated."""
        return Article.objects.active()

site.register(Article, ArticleIndex)

