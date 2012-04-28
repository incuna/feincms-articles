from haystack import indexes
from models import Article


class TempArticleIndex(indexes.SearchIndex):
    name = indexes.CharField(model_attr='title')
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Article

    def index_queryset(self):
        return self.get_model().objects.active()

try:
    # In haystack < 2.0 we need to explicitly register indexes
    from haystack import site
except ImportError:
    # In haystack >= 2.0 Indexes subclass indexes.Indexable
    class ArticleIndex(TempArticleIndex, indexes.Indexable):
        pass
else:
    class ArticleIndex(TempArticleIndex):
        def get_queryset(self):
            return self.index_queryset()

    site.register(Article, ArticleIndex)
