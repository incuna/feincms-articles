import re
from django import template
from django.forms.util import flatatt
from django.utils.safestring import mark_safe
from articles.models import Article, Category

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
            categories = Category.objects.filter(parent__isnull=True)
        else:
            if selected is not None:
                # is the selected category a descendant of 
                if current.get_descendants(include_self=True).filter(pk=selected.pk).count() > 0:
                    categories = current.children.all()


        if categories is not None:
            categories = categories.filter(article__in=Article.objects.active(user=user), article__isnull=False).distinct()

        t = template.loader.select_template(['articles/categories.html'])
        context.push()
        context['selected'] = selected
        context['categories'] = categories
        output = t.render(context)
        context.pop()

        return output


@register.tag()
def categories(parser, token):
    bits = token.split_contents() 

    args, kwargs = parse_tokens(parser, bits)

    return CategoriesNode(*args, **kwargs)


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

        user = None
        if 'request' in context:
            user = context['request'].user

        articles = Article.objects.active(user=user).select_related()

        if isinstance(category, (str,unicode,)):
            try:
                category = Category.objects.get(slug=category)
            except Category.DoesNotExist:
                category = None

        if category is not None:
            articles = articles.filter(category__in=category.get_descendants(include_self=True)).order_by(category.order_by)

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


class CalendarNode(template.Node):
    """
        Render a google calendar (iframe) embed.

        Usage:
            {% calendar category width="580" height="350" %}
    """

    COLOURS = ['D96666',
               'E67399',
               '8C66D9',
               '668CB3',
               '668CD9',
               '59BFB3',
               '65AD89',
               '4CB052',
               '8CBF40',
               'E0C240',
               'E6804D',
               'BE9494',
               'A992A9',
               '8997A5',
               '94A2BE',
               '85AAA5',
               'A7A77D',
               'C4A883',
               'C7561E',
               'B5515D',
               'C244AB',
               '603F99',
               '536CA6',
               '3640AD',
               '3C995B',
               '5CA632',
               '7EC225',
               'A7B828',
               'CF9911',
               'D47F1E',
               'B56414',
               '914D14',
               'AB2671',
               '9643A5',
               '4585A3',
               '737373',
               '41A587',
               'D1BC36',
               'AD2D2D',
              ]

    @staticmethod
    def colours(start = 0):
        """
        Returns a stream of colours, if the end of the list is reached then it starts back at the beginning.
        """
        while True:
            try:
                yield CalendarNode.COLOURS[start]
            except IndexError:
                start = 0
                yield CalendarNode.COLOURS[start]
            start += 1

    def __init__(self, category, attrs):
        self.category = category
        self.attrs = attrs

    def render(self, context):
        category = self.category.resolve(context)
        attrs = {}

        final_attrs = dict(style=" border-width:0 ", 
                           width="800", 
                           height="600", 
                           frameborder="0", 
                           scrolling="no")

        src_attrs = dict(showTitle="0", 
                         showCalendars="1", 
                         showTz="0", 
                         wkst="1", 
                         bgcolor="%23FFFFFF", 
                         ctz="Europe%2FLondon"
                        )

        if not isinstance(category, Category):
            try:
                category = Category.objects.get(local_url=category)
            except Category.DoesNotExist:
                return ''

        categories = []
        if category.calendar_id:
            categories.append(category)
        categories.extend(list(category.get_ancestors().filter(calendar_id__isnull=False)))

        if not categories:
            return ''

        for key in self.attrs:
            value = self.attrs[key].resolve(context) or self.attrs[key]
            if key in src_attrs:
                src_attrs[key] = value
            else:
                attrs[key] = value

        if attrs:
            final_attrs.update(attrs)

        colours = self.colours()
        src = "https://www.google.com/calendar/embed?%s" % ( '&'.join(["%s=%s" % pair for pair in src_attrs.items()]) )
        for c in categories:
            src += "&src=%s&color=%%23%s" % (c.calendar_id, colours.next())

        final_attrs['src'] = src

        return mark_safe(u'<iframe%s ></iframe>' % flatatt(final_attrs))

@register.tag()
def calendar(parser, token):
    bits = token.split_contents() 

    if len(bits) < 2:
        raise template.TemplateSyntaxError("'%s tag requires at least 1 arguments." % bits[0])

    category = parser.compile_filter(bits[1])
    dict = {}
    try:
        for pair in bits[2:]:
            pair = pair.split('=')
            dict[pair[0]] = parser.compile_filter(pair[1])
    except TypeError:
        raise template.TemplateSyntaxError('Bad arguments for tag "%s"' % bits[0])

    return CalendarNode(category, dict)


