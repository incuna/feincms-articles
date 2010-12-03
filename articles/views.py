# Create your views here. article_detail, article_category
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response
from models import Article, Category
from tagging.models import Tag, TaggedItem
from django.conf import settings
from django.http import HttpResponseRedirect
from django.db.models import Q


def article_detail(request, category_url, slug, extra_context=None):

    context = RequestContext(request)

    article = get_object_or_404(Article.objects.active(user=request.user), category__local_url=category_url, slug=slug)

    tags = Tag.objects.usage_for_queryset(Article.objects.filter(category__in=article.category.get_descendants(include_self=True)))

    if extra_context is not None:
        contect.update(extra_context)

    context.update({
        'object': article,
        'category' : article.category,
        'tags': tags,
    })
    
    return render_to_response('articles/article_detail.html', context)


def article_category(request, category_url=None, extra_context=None):
    context = RequestContext(request)
    
    articles = Article.objects.active(user=request.user) 
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

    tags = Tag.objects.usage_for_queryset(articles)
    tag = None
    if request.GET and 'tag' in request.GET:
        try:
            tag = Tag.objects.get(name=request.GET['tag'])
        except Tag.DoesNotExist:
            pass
        else:
            articles = TaggedItem.objects.get_union_by_model(articles, [tag])

    if extra_context is not None:
        contect.update(extra_context)

    context.update({
        'object_list': articles,
        'tags': tags,
        'tag': tag,
        'category': category,
    })
    
    return render_to_response('articles/article_list.html', context)

