from django.views.generic import DetailView, ListView

from models import Article


class ArticleDetail(DetailView):
    model = Article

    def get_queryset(self):
        return Article.objects.active()


class ArticleDetail(ListView):
    model = Article

    def get_queryset(self):
        return Article.objects.active()
