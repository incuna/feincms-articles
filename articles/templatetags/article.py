from django import template
from articles.models import Category

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

