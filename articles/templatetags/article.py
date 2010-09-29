from django import template
from django.forms.util import flatatt
from articles.models import Article, Category

register = template.Library()

@register.inclusion_tag('articles/categories.html')
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

#@register.inclusion_tag('articles/calendar.html')
#def calendar(category, include_children=False):
#    """
#    Render a google calendar iframe embed.
#    """

#    if not isinstance(category, Category):
#        category = Category.objects.get(local_url=category)

#   """
#   <iframe src="https://www.google.com/calendar/embed?showTitle=0&amp;showCalendars=0&amp;showTz=0&amp;height=350&amp;wkst=1&amp;bgcolor=%23FFFFFF&amp;src=fkkq7cgbjk7nk32j10ug61oq04%40group.calendar.google.com&amp;color=%23856508&amp;ctz=Europe%2FLondon" style=" border-width:0 " width="580" height="350" frameborder="0" scrolling="no"></iframe> 
#   """

#    return {'category': category,
#            'rl': categories,
#           }


class CalendarNode(template.Node):
    """
        Render a google calendar (iframe) embed.

        Usage:
            {% calendar category width="580" height="350" %}
    """

    src

    def __init__(self, category, attrs):
        self.category = category
        self.attrs = attrs

    def render(self, context):
        category = self.category.resolve(context)
        attrs = {}

        final_attrs = dict(style=" border-width:0 ", width="580", height="350", frameborder="0", scrolling="no")

        src_attrs = dict(showTitle="0", 
                         showCalendars="0", 
                         showTz="0", 
                         height="350", 
                         wkst="1", 
                         bgcolor="%23FFFFFF", 
                         #src="fkkq7cgbjk7nk32j10ug61oq04%40group.calendar.google.com", 
                         #color="%23856508", 
                         ctz="Europe%2FLondon"
                        )


        categories = []
        if category.calendar_url:
            categories.append(category)
        categories.extend([for c in category.get_ancestors().filter(calendar_url__isnull=False)])

        if not categories:
            return ''

        for key in self.attrs:
            value = self.attrs[key].resolve(context) or self.attrs[key]
            if key in src_attrs:
                src_attrs[key] = value
            else:
                attrs[key] = value

        #t = template.loader.select_template(['articles/calendar.html'])
        #context.push()
        #context['category'] = category
        #context['attrs'] = attrs
        #output = t.render(context)
        #context.pop()

        #return output

        if attrs:
            final_attrs.update(attrs)

        src = "https://www.google.com/calendar/embed?%s" % ( ["%s=%s" % pair for pair in src_attrs.items()].join('&amp;') )
        for c in categories:
            src += "&amp;src=%s&amp;color=%%23%s" % (c.calendar_url, '856508')
        
        attrs['src'] = src

        return mark_safe(u'<iframe%s ></iframe>' % flatatt(final_attrs))


    """
<iframe src="https://www.google.com/calendar/embed?showTitle=0&amp;showTz=0&amp;height=350&amp;wkst=1&amp;bgcolor=%23FFFFFF&amp;src=calendars%40incuna.com&amp;color=%23691426&amp;src=fkkq7cgbjk7nk32j10ug61oq04%40group.calendar.google.com&amp;color=%23856508&amp;src=en.uk%23holiday%40group.v.calendar.google.com&amp;color=%23182C57&amp;ctz=Europe%2FLondon" style=" border-width:0 " width="580" height="350" frameborder="0" scrolling="no"></iframe>
    """

@register.tag()
def calendar(parser, token):
    bits = token.split_contents() 

    if len(bits) < 2:
        raise template.TemplateSyntaxError("'%s tag requires at least 1 arguments." % bits[0])
    if bits[2] == 'as':
        varname = bits[3]
        firstkey = 4
        #raise template.TemplateSyntaxError("'2nd argument to %s tag must be 'as'." % bits[0])
    else:
        firstkey = 2
        varname = None

    category = parser.compile_filter(bits[1])
    dict = {}
    try:
        for pair in bits[2:]:
            pair = pair.split('=')
            dict[pair[0]] = parser.compile_filter(pair[1])
    except TypeError:
        raise template.TemplateSyntaxError('Bad arguments for tag "%s"' % bits[0])

    return CalendarNode(category, dict)


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


