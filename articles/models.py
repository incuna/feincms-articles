from datetime import datetime
from django.db import models
from django.db.models import Q, signals
from denorm import denormalized, depend_on_related
from django.utils.translation import ugettext_lazy as _
from incuna.db.models import AutoSlugField
from tagging.fields import TagField

from django.conf import settings

try:
    from djangogcal.adapter import CalendarAdapter, CalendarEventData
    from djangogcal.observer import CalendarObserver
    DJANGOCAL_SYNC = True
except ImportError:
    DJANGOCAL_SYNC = False


from feincms.models import Base
from feincms.management.checker import check_database_schema
from feincms.content.medialibrary.models import MediaFileContent
from feincms.content.richtext.models import RichTextContent

import mptt

class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = AutoSlugField(max_length=255,populate_from="name",help_text='This will be automatically generated from the name',unique=True,editable=True)
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children')
    calendar_feed = models.CharField(max_length=255, blank=True, null=True, 
                                     help_text='Google calendar feed url e.g. https://www.google.com/calendar/feeds/username@gmail.com/private/full/')

    @denormalized(models.CharField, max_length=255, editable=False, default='', db_index=True)
    @depend_on_related('self',type='forward')
    def local_url(self):
        if self.parent:
            root = self.parent.local_url
        else:
            root = ''
        return u'%s%s/' % (root, self.slug)

    class Meta:
        ordering = ['tree_id', 'lft']
        verbose_name_plural = 'categories'
 
    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('article_category', (self.local_url,))

mptt.register(Category)

class ArticleManager(models.Manager):
    def active(self):
        """Active component"""
        return self.filter(Q(publication_date__lte=datetime.now()) & \
            (Q(publication_end_date__isnull=True) | Q(publication_end_date__gt=datetime.now())))

class Article(Base): 
    title = models.CharField(max_length=255)
    slug = AutoSlugField(max_length=255,populate_from="title",help_text='This will be automatically generated from the name',unique=True,editable=True)
    summary = models.TextField(null=True, blank=True)
    publication_date = models.DateTimeField(_('Publication date'), default=datetime.now,)
    publication_end_date = models.DateTimeField(_('Publication end date'), null=True, blank=True,)
    category = models.ForeignKey(Category)
    tags = TagField(null=True, blank=True)

    class Meta:
        ordering = ('-publication_date',)
        get_latest_by = 'publication_date'

    objects = ArticleManager()

    def __unicode__(self):
        return u"%s" % (self.title)


    @models.permalink
    def get_absolute_url(self):
        return ('article_detail', (), {
                'category_url': self.category.local_url,
                'slug': self.slug,
                })

Article.register_regions(
    ('main', 'Main region'),
    )
Article.create_content_type(RichTextContent)
Article.create_content_type(MediaFileContent, POSITION_CHOICES=(('default', _('Default')),))


if DJANGOCAL_SYNC:
    class ArticleCalendarAdapter(CalendarAdapter):
        """
        A calendar adapter for the Showing model.
        """

        def get_event_data(self, instance):
            """
            Returns a CalendarEventData object filled with data from the adaptee.
            """

            return CalendarEventData(
                start=instance.publication_date,
                end=instance.publication_end_date or instance.publication_date,
                title=instance.title,
                content=instance.summary
            )

        def get_feed_url(self, instance):
            try:
                return instance.category.calendar_feed
            except IndexError:
                return None

        def can_save(self, instance):
            return self.get_feed_url(instance) is not None

        def can_delete(self, instance):
            return self.get_feed_url(instance) is not None


    observer = CalendarObserver(
        email=settings.CALENDAR_EMAIL,
        password=settings.CALENDAR_PASSWORD,
    )
    observer.observe(Article, ArticleCalendarAdapter())

