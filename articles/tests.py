import datetime
import warnings

from django.core.urlresolvers import reverse
from django.test import TestCase

from .models import Article


def find(f, seq):
    """
    Return first item in sequence where f(item) == True.
    e.g.
    fred = find(lambda person: person.name == 'Fred', peeps)
    """
    for item in seq:
        if f(item):
            return item


class ArticleAccessTests(TestCase):
    fixtures = ['articles_data.json',]
    def test_article_index(self):
        response = self.client.get(reverse('article_index'))
        for article in Article.objects.active():
            self.assertContains(response, article.title)

    def test_article_detail(self):
        response = self.client.get(reverse('article_detail', args=['test-article',]))


        article = Article.objects.active().get(slug='test-article')
        self.assertContains(response, article.title)

class ArticleActiveTests(TestCase):
    fixtures = ['articles_data.json',]
    def test_article_active(self):
        response = self.client.get(reverse('article_index'))


        inactive_articles = Article.objects.exclude(pk__in=[a[0] for a in Article.objects.active().values_list('pk')])
        assert(inactive_articles)
        for article in inactive_articles:
            self.assertNotContains(response, article.title)

    def test_article_views_404(self):
        response = self.client.get(reverse('article_detail', args=['inactive-article',]))
        self.assertEquals(response.status_code, 404)

# extension related tests
class ArticleDatePublisherTests(TestCase):
    fixtures = ['articles_datepublisher_data.json',]

    def setUp(self, *args, **kwargs):
        if bool(find(lambda f: f.name == 'publication_date', Article._meta.local_fields)) \
           and bool(find(lambda f: f.name == 'publication_end_date', Article._meta.local_fields)):
            self.skip = False
        else: 
            warnings.warn("Skipping datepublisher tests. Extension not registered")
            self.skip = True

    def test_publication_date(self):
        if self.skip:
            return

        article = Article.objects.active().get(slug='publication-date-test')
        article.publication_date = datetime.datetime.now() + datetime.timedelta(1)
        article.save()

        response = self.client.get(reverse('article_detail', args=['publication-date-test',]))
        self.assertEquals(response.status_code, 404)


        article.publication_date = datetime.datetime.now() + datetime.timedelta(-1)
        article.publication_end_date = datetime.datetime.now() + datetime.timedelta(-1)
        article.save()

        response = self.client.get(reverse('article_detail', args=['publication-date-test',]))
        self.assertEquals(response.status_code, 404)


class ArticleTagsTests(TestCase):
    fixtures = ['articles_tags_data.json',]

    def setUp(self, *args, **kwargs):
        if bool(find(lambda f: f.name == 'tags', Article._meta.many_to_many)):
            self.skip = False
        else: 
            warnings.warn("Skipping tags tests. Extension not registered")
            self.skip = True

    def test_tags(self):
        if self.skip:
            return

        article = Article.objects.active().get(slug='tag-test')
        article.tags.add("test", "testing")

        response = self.client.get(reverse('article_tagged_list', args=['test',]))
        self.assertContains(response, article.title)

    def test_tags_404(self):
        response = self.client.get(reverse('article_tagged_list', args=['tag_does_not_exist',]))
        self.assertEquals(response.status_code, 404)

