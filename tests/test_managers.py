from articles.models import Article
from django.test import TestCase

from .factories import ArticleFactory


class TestManager(TestCase):

    def test_active(self):
        active = ArticleFactory.create(active=True)
        ArticleFactory.create(active=False)

        qs = Article.objects.active()

        self.assertSequenceEqual(qs, [active])
