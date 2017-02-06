from django.db.models.fields import FieldDoesNotExist
from haystack import indexes

from .models import Article


class TempArticleIndex(indexes.SearchIndex):
    title = indexes.CharField(model_attr='title')
    name = indexes.CharField(model_attr='title')
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Article

    def index_queryset(self, using=None):
        return self.get_model().objects.active()

    def get_updated_field(self, **kwargs):
        try:
            self.get_model()._meta.get_field('modification_date')
        except FieldDoesNotExist:
            return None
        else:
            return 'modification_date'


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
