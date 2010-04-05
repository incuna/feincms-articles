from django import template
from articles.models import Article, Category

register = template.Library()

def categories(selected=None, current=None):
    categories = None
    if current is None:
        categories = Category.objects.filter(parent__isnull=True)
    else:
        if selected is not None:
            # is the selected category a descebdant of 
            if current.get_descendants(include_self=True).filter(pk=selected.pk).count() > 0:
                categories = current.children.all()

    return {'selected': selected,
            'categories': categories,
           }

register.inclusion_tag('articles/categories.html')(categories)

def articles(category=None, limit=None):
    articles = Article.objects.active()

    if isinstance(category, (str,unicode,)):
        try:
            category = Category.objects.get(slug=category)
        except Category.DoesNotExist:
            category = None

    if category is not None:
        articles = articles.filter(category__in=category.get_descendants(include_self=True))

    if limit is not None:
        articles = articles[:limit]

    return {'category': category,
            'articles': articles,
           }

register.inclusion_tag('articles/articles.html')(articles)

