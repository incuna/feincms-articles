from datetime import datetime
from django.db import models
from django.db.models import Q, signals
from denorm import denormalized, depend_on_related
from django.utils.translation import ugettext_lazy as _
from django.contrib.sites.models import Site
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
from feincms.content.medialibrary.models import MediaFileContent
from feincms.content.richtext.models import RichTextContent

import mptt

class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = AutoSlugField(max_length=255,populate_from="name",help_text='This will be automatically generated from the name',unique=True,editable=True)
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children')
    calendar_id = models.EmailField('calendar id', max_length=255, blank=True, null=True, 
                                    help_text='Google Calendar Id e.g. username@gmail.com')

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


    @property
    def calendar_feed(self):
        if self.calendar_id:
            return "/calendar/feeds/%s/private/full/" % (self.calendar_id,)
        else:
            return None

mptt.register(Category)

class ArticleManager(models.Manager):
    def active(self, user=None):
        """Active component"""
        articles =  self.filter(Q(publication_date__lte=datetime.now()) & \
            (Q(publication_end_date__isnull=True) | Q(publication_end_date__gt=datetime.now())))

        if user is not None and user.is_authenticated():
            articles = articles.filter(Q(access_groups__isnull=True) | Q(access_groups__in=user.groups.all()))
        else:
            articles = articles.filter(access_groups__isnull=True)

        return articles
        


class Article(Base): 
    title = models.CharField(max_length=255)
    slug = AutoSlugField(max_length=255,populate_from="title",help_text='This will be automatically generated from the name',unique=True,editable=True)
    summary = models.TextField(null=True, blank=True)
    publication_date = models.DateTimeField(_('Publication date'), default=datetime.now,)
    publication_end_date = models.DateTimeField(_('Publication end date'), null=True, blank=True,)
    category = models.ForeignKey(Category)
    tags = TagField(null=True, blank=True)
    thumbnail = models.ImageField(max_length=250, upload_to="articles/thumbnails", null=True, blank=True)

    access_groups  = models.ManyToManyField("auth.Group", null=True, blank=True,
                                            help_text='Users must be logged in and a member of the group(s) to access this article.', )

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

    @property
    def is_active(self):
        return Article.objects.active().filter(pk=self.pk).count() > 0

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

            content = instance.summary
            if instance.content.main:
                content += '<p><a href="%s%s">Event home page</a></p>' % (Site.objects.get_current().domain, instance.get_absolute_url(),)

            print content

            return CalendarEventData(
                start=instance.publication_date,
                end=instance.publication_end_date or instance.publication_date,
                title=instance.title,
                content=content
            )

        def get_feed_url(self, instance):
            try:
                return instance.category.calendar_feed
            except IndexError:
                return None

        def can_save(self, instance):
            return self.get_feed_url(instance) is not None and instance.is_active

        def can_delete(self, instance):
            return self.get_feed_url(instance) is not None


    observer = CalendarObserver(
        email=settings.CALENDAR_EMAIL,
        password=settings.CALENDAR_PASSWORD,
    )
    observer.observe(Article, ArticleCalendarAdapter())

