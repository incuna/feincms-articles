import mptt
from datetime import datetime
from django.db import models
from denorm import denormalized, depend_on_related
from incuna.db.models import AutoSlugField

class CategoryManager(models.Manager):

    def active_query(self, user=None):
        now = datetime.now()
        query = (Q(publication_date__lte=now) & \
                  (Q(publication_end_date__isnull=True) | Q(publication_end_date__gt=now)))

        if user is not None and user.is_authenticated():
            query = query & (Q(access_groups__isnull=True) | Q(access_groups__in=user.groups.all()))
        else:
            query = query & Q(access_groups__isnull=True)

        return query

    def active(self, user=None):
        """Active categories (containing active articles)"""

        return self.filter(self.active_query(user=user)).distinct()

class Category(models.Model):
    ORDER_BY_CHOICES = (('publication_date', 'Publication date (oldest first)'),
                        ('-publication_date', 'Publication date (newest first)'),
                        ('title', 'Title A-Z'),
                        ('-title', 'Title Z-A'),
                       )

    name = models.CharField(max_length=255)
    slug = AutoSlugField(max_length=255,populate_from="name",help_text='This will be automatically generated from the name',unique=True,editable=True)
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children')
    order_by = models.CharField('articles order', max_length=30, choices=ORDER_BY_CHOICES, help_text='The order of article items in this category.', default='-publication_date')

    access_groups  = models.ManyToManyField("auth.Group", null=True, blank=True,
                                            help_text='Users must be logged in and a member of the group(s) to access this group.', )

    @denormalized(models.CharField, max_length=255, editable=False, default='', db_index=True)
    @depend_on_related('self',type='forward')
    def local_url(self):
        if self.parent:
            root = self.parent.local_url
        else:
            root = ''
        return u'%s%s/' % (root, self.slug)

    @denormalized(models.DateTimeField, editable=False, null=True, blank=True,)
    @depend_on_related('self',type='forward')
    def publication_date(self):
       try:
           return self.descendant_articles.annotate(models.Min('publication_date'))[0].publication_date__min 
       except IndexError:
           return None
    @denormalized(models.DateTimeField, editable=False, null=True, blank=True,)
    @depend_on_related('self',type='forward')
    def publication_end_date(self):
       try:
           return self.descendant_articles.annotate(models.Min('publication_end_date'))[0].publication_end_date__min 
       except IndexError:
           return None

    @property
    def descendant_articles(self):
        return Article.objects.filter(category__in=self.get_descendants(include_self=True))

    objects = CategoryManager()

    class Meta:
        app_label = 'articles'
        ordering = ['tree_id', 'lft']
        verbose_name_plural = 'categories'

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('article_category', (self.local_url,))

mptt.register(Category)

