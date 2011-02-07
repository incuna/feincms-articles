import re
from django import template
from django.forms.util import flatatt
from django.utils.safestring import mark_safe
from articles.modules.category.models import Category
from articles.models import Article

from incuna.template.defaulttags import parse_tokens

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


from tagging.models import Tag

class TagsForQuerySetNode(template.Node):
    def __init__(self, queryset, context_var, counts):
        self.queryset = template.Variable(queryset)
        self.context_var = context_var
        self.counts = counts

    def render(self, context):
        queryset = self.queryset.resolve(context)
        context[self.context_var] = Tag.objects.usage_for_queryset(queryset, counts=self.counts)
        return ''

@register.tag()
def tags_for_queryset(parser, token):
    """
    Retrieves a list of ``Tag`` objects associated with a given model
    and stores them in a context variable.

    Usage::

       {% tags_for_query [queryset] as [varname] %}

    Extended usage::

       {% tags_for_query [queryset] as [varname] with counts %}

    If specified - by providing extra ``with counts`` arguments - adds
    a ``count`` attribute to each tag containing the number of
    instances of the given model which have been tagged with it.

    Examples::

       {% tags_for_query products as prod_tags %}
       {% tags_for_query products as prod_tags with counts %}

    """
    bits = token.contents.split()
    len_bits = len(bits)
    if len_bits not in (4, 6):
        raise template.TemplateSyntaxError(_('%s tag requires either three or five arguments') % bits[0])
    if bits[2] != 'as':
        raise template.TemplateSyntaxError(_("second argument to %s tag must be 'as'") % bits[0])
    if len_bits == 6:
        if bits[4] != 'with':
            raise template.TemplateSyntaxError(_("if given, fourth argument to %s tag must be 'with'") % bits[0])
        if bits[5] != 'counts':
            raise template.TemplateSyntaxError(_("if given, fifth argument to %s tag must be 'counts'") % bits[0])
    if len_bits == 4:
        return TagsForQuerySetNode(bits[1], bits[3], counts=False)
    else:
        return TagsForQuerySetNode(bits[1], bits[3], counts=True)

