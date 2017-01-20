import factory

from articles.models import Article


class ArticleFactory(factory.DjangoModelFactory):
    title = factory.Sequence('{}'.format)
    slug = factory.Sequence('{}'.format)

    class Meta:
        model = Article
