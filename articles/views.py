from django.views.generic import DetailView, ListView

from models import Article


class AppContentMixin(object):
    def render_to_response(self, context, **response_kwargs):
        """
        Returns the template tuple needed for FeinCMS App Content.
        """
        return (self.get_template_names(), context)


class ArticleDetail(AppContentMixin, DetailView):
    model = Article

    def get_queryset(self):
        return Article.objects.active()


class ArticleList(AppContentMixin, ListView):
    model = Article

    def get_queryset(self):
        return Article.objects.active()
