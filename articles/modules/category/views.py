from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response
from articles.views import ArticleDetail
from articles.models import Article
from models import Category
#from tagging.models import Tag, TaggedItem
from django.conf import settings
from django.http import HttpResponseRedirect


class CategoryArticleDetail(ArticleDetail):
    template_name = "articles/category_article_detail.html"
    def get_queryset(self):
        return super(CategoryArticleDetail, self).get_queryset().filter(category__local_url=self.kwargs['category_url'])
article_detail = CategoryArticleDetail.as_view()

def article_category(request, category_url=None, extra_context=None):
    context = RequestContext(request)

    articles = Article.objects.active()
    if category_url is not None:
        category = get_object_or_404(Category.objects.active(user=request.user), local_url=category_url)
        if getattr(settings, 'ARTICLE_SHOW_DESCENDANTS', False):
            articles = articles.filter(category__in=category.get_descendants(include_self=True)).order_by(category.order_by)
        else:
            articles = articles.filter(category=category).order_by(category.order_by)
    else:
        if getattr(settings, 'ARTICLE_SHOW_FIRST_CATEGORY', False):
            # Redirect to the first category
            try:
                return HttpResponseRedirect(Category.objects.active(user=request.user)[0].get_absolute_url())
            except IndexError, e:
                pass
        category = None

    #tag = None
    #if request.GET and 'tag' in request.GET:
    #    try:
    #        tag = Tag.objects.get(name=request.GET['tag'])
    #    except Tag.DoesNotExist:
    #        pass
    #    else:
    #        articles = TaggedItem.objects.get_union_by_model(articles, [tag])

    if extra_context is not None:
        contect.update(extra_context)

    context.update({
        'object_list': articles,
        #'tag': tag,
        'category': category,
    })
    
    return render_to_response('articles/category_article_list.html', context)


