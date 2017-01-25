from incuna_test_utils.testcases.urls import URLTestCase

from articles.views import ArticleDetail, ArticleList


class TestUrl(URLTestCase):

    def test_article_index(self):
        self.assert_url_matches_view(
            view=ArticleList,
            expected_url='/',
            url_name='article_index',
        )

    def test_article_detail(self):
        slug = 'ellobiidae'
        self.assert_url_matches_view(
            view=ArticleDetail,
            expected_url='/{}/'.format(slug),
            url_name='article_detail',
            url_kwargs={'slug': slug},
        )
