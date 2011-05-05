from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response
from models import Article

def article_detail(request, article, template='articles/article_detail.html', extra_context=None):

    context = RequestContext(request)

    if isinstance(article, basestring):
        article = get_object_or_404(Article.objects.active(user=request.user), slug=article)

    if extra_context is not None:
        context.update(extra_context)

    context.update({
        'object': article,
    })
    
    return render_to_response(template, context)


def article_list(request, template='articles/article_list.html', extra_context=None):
    context = RequestContext(request)
    
    articles = Article.objects.active(user=request.user) 

    if extra_context is not None:
        context.update(extra_context)

    context.update({
        'object_list': articles,
    })
    
    return render_to_response(template, context)

