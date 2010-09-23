from django.db import models
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.template import RequestContext
from django.template.loader import render_to_string

class ArticleContent(models.Model):

    class Meta:
        abstract = True

    @classmethod
    def initialize_type(cls):
        if 'articles' not in settings.INSTALLED_APPS:
            raise ImproperlyConfigured, "You have to add 'articles' to your INSTALLED_APPS before creating a %s" % cls.__name__

        cls.add_to_class('category', models.ForeignKey('articles.Category',
                                                       related_name='%s_%s_set' % (cls._meta.app_label, cls._meta.module_name)
        ))

    def render(self, request=None, **kwargs):
        if request is not None:
            context = RequestContext(request)
            context.update({ 'content': self })
        else:
            context = { 'content': self }

        return render_to_string(['content/articles/category_%s.html' % self.category.slug,
                                 'content/articles/default.html',
                                ], context)
