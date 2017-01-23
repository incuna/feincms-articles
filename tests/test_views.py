from django.urls import reverse
from django.test import modify_settings, TestCase

from .factories import ArticleFactory


class TestView(TestCase):
    slug_name = 'ellobiidae'

    @modify_settings(INSTALLED_APPS={'append': ['tests']})
    def test_index_response_ok(self):
        response = self.client.get(reverse('article_index'))
        self.assertEqual(response.status_code, 200)

    @modify_settings(INSTALLED_APPS={'append': ['tests']})
    def test_detail_response_ok(self):
        article = ArticleFactory.create(slug=self.slug_name)
        url = reverse('article_detail', kwargs={'slug': self.slug_name})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_detail_not_found(self):
        url = reverse('article_detail', kwargs={'slug': self.slug_name})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)
