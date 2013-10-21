from django.db import models
from django.template.loader import render_to_string

from .models import Article


class ArticleList(models.Model):
    number = models.IntegerField()

    class Meta:
        abstract = True

    def get_queryset_for_render(self):
        return Article.objects.all()

    def render(self, **kwargs):
        context = {
            'object_list': self.get_queryset_for_render()[:self.number],
            'request': kwargs.get('request'),
        }
        return render_to_string('content/articles/list.html', context)
