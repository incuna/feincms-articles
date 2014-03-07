import mptt
from denorm import denormalized, depend_on_related
from django.conf import settings
from django.core.urlresolvers import get_callable
from django.db import models
from django.db.models import Q
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from feincms.admin import tree_editor as editor
from feincms.content.application import models as app_models

from articles.models import Article


class CategoryManager(models.Manager):

    def active_query(self, user=None):

        if user is not None and user.is_authenticated():
            query = Q(access_groups__isnull=True) | Q(access_groups__in=user.groups.all())
        else:
            query = Q(access_groups__isnull=True)

        return query

    def active(self, user=None):
        """Active categories (containing active articles)"""

        return self.filter(self.active_query(user=user)).distinct()


@python_2_unicode_compatible
class Category(models.Model):
    ORDER_BY_CHOICES = (('publication_date', _('Publication date (oldest first)')),
                        ('-publication_date', _('Publication date (newest first)')),
                        ('title', _('Title A-Z')),
                        ('-title', _('Title Z-A')),
                       )

    name = models.CharField(_('name'), max_length=255)
    slug = models.SlugField(_('slug'), max_length=255, help_text=_('This will be automatically generated from the name'),unique=True,editable=True)
    parent = models.ForeignKey('self', verbose_name=_('parent'), blank=True, null=True, related_name='children')
    order_by = models.CharField(_('articles order'), max_length=30, choices=ORDER_BY_CHOICES, help_text=_('The order of article items in this category.'), default='-publication_date')

    access_groups  = models.ManyToManyField("auth.Group", verbose_name=_('access groups'), null=True, blank=True,
                                            help_text=_('Users must be logged in and a member of the group(s) to access this group.'), )

    @denormalized(models.CharField, max_length=255, editable=False, default='', db_index=True)
    @depend_on_related('self',type='forward')
    def local_url(self):
        if self.parent:
            root = self.parent.local_url
        else:
            root = ''
        return u'%s%s/' % (root, self.slug)

    @property
    def descendant_articles(self):
        return Article.objects.filter(category__in=self.get_descendants(include_self=True))

    objects = CategoryManager()

    class Meta:
        app_label = 'articles'
        ordering = ['tree_id', 'lft']
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    def __str__(self):
        return self.name

    @app_models.permalink
    def get_absolute_url(self):
        return ('article_category', 'articles.urls', (self.local_url,))

mptt.register(Category)


ModelAdmin = get_callable(getattr(settings, 'CATEGORY_MODELADMIN_CLASS', 'django.contrib.admin.ModelAdmin'))


class CategoryAdmin(editor.TreeEditor, ModelAdmin):
    list_display = ['name', 'order_by']
    list_filter = ['parent',]
    prepopulated_fields = {
        'slug': ('name',),
    }
