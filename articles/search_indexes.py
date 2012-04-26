from haystack import indexes
from models import Article


class ArticleIndex(indexes.SearchIndex):
    name = indexes.CharField(model_attr='title')
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Article

    def get_queryset(self):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.active()


# In haystack < 2.0 we need to explicitly register indexes
try:
    from haystack import site
except ImportError:
    pass
else:
    site.register(Article, ArticleIndex)
