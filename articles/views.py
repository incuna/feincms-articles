from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response
#from tagging.models import Tag, TaggedItem
from models import Article



def article_detail(request, article, template='articles/article_detail.html', extra_context=None):

    context = RequestContext(request)

    if isinstance(article, basestring):
        article = get_object_or_404(Article.objects.active(user=request.user), slug=article)

    #tags = Tag.objects.usage_for_queryset(Article.objects.filter(category__in=article.category.get_descendants(include_self=True)))

    if extra_context is not None:
        contect.update(extra_context)

    context.update({
        'object': article,
        #'category' : article.category,
        #'tags': tags,
    })
    
    return render_to_response(template, context)


def article_list(request, template='articles/article_list.html', extra_context=None):
    context = RequestContext(request)
    
    articles = Article.objects.active(user=request.user) 

    #tags = Tag.objects.usage_for_queryset(articles)
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
        #'tags': tags,
        #'tag': tag,
        #'category': category,
    })
    
    return render_to_response(template, context)

