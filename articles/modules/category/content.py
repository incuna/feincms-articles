from django import forms
from django.db import models
from django.contrib.admin.widgets import AdminRadioSelect
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from feincms.admin.item_editor import ItemEditorForm

from articles.models import Article


class ArticleCategoryList(models.Model):
    """
    List articles belonging to the selected category.
    """
    category = models.ForeignKey('articles.Category')
    number = models.IntegerField()

    class Meta:
        abstract = True
        verbose_name = _('article category list')

    @classmethod
    def initialize_type(cls, LAYOUT_CHOICES=None):

        cls.add_to_class('layout', models.CharField(_('Layout'),
                                                    max_length=10, choices=LAYOUT_CHOICES,
                                                    default=LAYOUT_CHOICES[0][0]))

        class ArticleCategoryListForm(ItemEditorForm):
            layout = forms.ChoiceField(choices=LAYOUT_CHOICES,
                                       initial=LAYOUT_CHOICES[0][0], label=_('Layout'),
                                       widget=AdminRadioSelect(attrs={'class': 'radiolist'}))

        cls.feincms_item_editor_form = ArticleCategoryListForm
        cls.form = ArticleCategoryListForm

    def get_queryset_for_render(self):
        return Article.objects.filter(category=self.category)

    def render(self, **kwargs):
        context = {
            'object_list': self.get_queryset_for_render()[:self.number],
            'request': kwargs.get('request'),
            'content': self,
        }
        return render_to_string([
            'content/articles/category/%s/%s.html' % (self.region, self.layout),
            'content/articles/category/%s/default.html' % self.region,
            'content/articles/category/%s.html' % self.layout,
            'content/articles/category/default.html',
            ], context)


class ArticleList(models.Model):
    """
    List articles belonging to any of the selected categories.
    If no categories are selected then list all articles.
    """
    number = models.IntegerField()
    categories = models.ManyToManyField('articles.Category', null=True, blank=True)

    class Meta:
        abstract = True
        verbose_name = _('article list')

    def get_queryset_for_render(self):
        articles = Article.objects.all()
        if self.categories.count():
            articles = articles.filter(category__in=self.categories.all())
        return articles

    def render(self, **kwargs):
        context = {
            'object_list': self.get_queryset_for_render()[:self.number],
            'request': kwargs.get('request'),
            'content': self,
        }
        return render_to_string(['content/articles/%s/list.html' % self.region,
                                 'content/articles/list.html',
                                ],
                                context)
