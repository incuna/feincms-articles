# Create your views here. article_detail, article_category
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response
from models import Article, Category


def article_detail(request, category_url, slug, extra_context=None):

    context = RequestContext(request)

    article = get_object_or_404(Article.objects.active(), category__local_url=category_url, slug=slug)


    if extra_context is not None:
        contect.update(extra_context)

    context.update({
        'object': article,
    })
    
    return render_to_response('articles/article_detail.html', context)


def article_category(request, category_url=None, extra_context=None):
    context = RequestContext(request)
    
    articles = Article.objects.active()
    if category_url is not None:
        category = get_object_or_404(Category, local_url=category_url)
        articles = articles.filter(category__in=category.get_descendants(include_self=True))
    else:
        category = None

    if extra_context is not None:
        contect.update(extra_context)

    context.update({
        'object_list': articles,
        'category': category,
    })
    
    return render_to_response('articles/article_category.html', context)

