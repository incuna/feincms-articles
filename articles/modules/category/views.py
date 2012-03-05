from django.shortcuts import get_object_or_404
from articles.views import ArticleDetail, ArticleList
from articles.models import Article
from models import Category
#from tagging.models import Tag, TaggedItem
from django.conf import settings
from django.http import HttpResponseRedirect


class CategoryArticleDetail(ArticleDetail):
    template_name = "articles/category_article_detail.html"
    def get_queryset(self):
        return super(CategoryArticleDetail, self).get_queryset().filter(category__local_url=self.kwargs['category_url'])


class CategoryArticleList(ArticleList):
    template_name = "articles/category_article_list.html"
    def get_context_data(self, **kwargs):
        context = super(CategoryArticleList, self).get_context_data(**kwargs)

        category = None
        if 'category_url' in self.kwargs:
            # TODO: This is done TWICE
            category = get_object_or_404(Category.objects.active(), local_url=self.kwargs['category_url'])
        
        context['category'] = category

        return context
        
    def get_queryset(self):

        articles = super(CategoryArticleList, self).get_queryset()
        #.filter(category__local_url=self.kwargs['category_url'])
        if 'category_url' in self.kwargs:
            # TODO: This is done TWICE
            category = get_object_or_404(Category.objects.active(), local_url=self.kwargs['category_url'])

            if getattr(settings, 'ARTICLE_SHOW_DESCENDANTS', False):
                articles = articles.filter(category__in=category.get_descendants(include_self=True)).order_by(category.order_by)
            else:
                articles = articles.filter(category=category).order_by(category.order_by)
        else:
            if getattr(settings, 'ARTICLE_SHOW_FIRST_CATEGORY', False):
                # Redirect to the first category
                try:
                    return HttpResponseRedirect(Category.objects.active()[0].get_absolute_url())
                except IndexError, e:
                    pass
            category = None

        return articles
