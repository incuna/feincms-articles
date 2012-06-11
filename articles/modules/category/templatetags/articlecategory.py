from django import template

from articles.modules.category.models import Category
from articles.utils import parse_tokens

register = template.Library()

class CategoriesNode(template.Node):
    """
        Output a list of categories.

        Usage:
            {% categories %}
    """
    def __init__(self, selected=None, current=None):
        self.selected = selected
        self.current = current

    def render(self, context):
        selected = self.selected and self.selected.resolve(context)
        current = self.current and self.current.resolve(context)

        user = 'request' in context and context['request'].user or None
        categories = None
        if current is None:
            categories = Category.objects.active(user=user).filter(parent__isnull=True)
        else:
            if selected is not None:
                # is the selected category a descendant of 
                if current.get_descendants(include_self=True).filter(pk=selected.pk).count() > 0:
                    categories = current.children.filter(Category.objects.active_query(user=user))

        if categories is not None:
            categories = categories.distinct()

        t = template.loader.select_template(['articles/categories.html'])
        context.push()
        context['selected'] = selected
        context['categories'] = categories
        output = t.render(context)
        context.pop()

        return output


@register.tag()
def articlecategories(parser, token):
    bits = token.split_contents() 

    args, kwargs = parse_tokens(parser, bits)

    return CategoriesNode(*args, **kwargs)

