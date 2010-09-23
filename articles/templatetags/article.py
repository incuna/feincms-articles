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

class ArticlesNode(template.Node):
    """
        Output a list of articles.
        If as varname is specified then add the result to the context.

        Usage:
            {% articles %}
            OR
            {% articles category %}
            OR
            {% articles category limit %}
            OR
            {% articles as artilce_list %}
            OR
            {% articles category as artilce_list %}
            OR
            {% articles category limit as artilce_list %}
    """
    def __init__(self, category=None, limit=None, varname=None):
        self.category = category
        self.limit = limit
        self.varname = varname

    def render(self, context):
        category = self.category and self.category.resolve(context)
        limit = self.limit and self.limit.resolve(context)


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


        if self.varname is not None:
            context[self.varname] = articles
            return ''
        else:
            t = template.loader.select_template(['articles/articles.html'])
            context.push()
            context['category'] = category
            context['articles'] = articles
            output = t.render(context)
            context.pop()

            return output


@register.tag()
def articles(parser, token):
    bits = token.split_contents() 

    if bits[-2] == 'as':
        varname = bits[-1]
        args = bits[1:-2]
    else:
        args = bits[1:]
        varname = None

    return ArticlesNode(*map(parser.compile_filter, args), varname=varname)


