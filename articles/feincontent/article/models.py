from django.db import models
from django.conf import settings
from incunafein.content import BaseFkeyContent

class ArticleFkeyContent(BaseFkeyContent):
    
    class Meta:
        abstract = True
            
    def template_hierarchy(self):
        return ['content/articles/category_%s.html' % self.category.slug,
                'content/articles/default.html',
               ]

class ArticleCalendarFkeyContent(BaseFkeyContent):
    
    class Meta:
        abstract = True
            
    @classmethod
    def initialize_type(cls):
        if cls.app_label not in settings.INSTALLED_APPS:
            raise ImproperlyConfigured, "You have to add '%s' to your INSTALLED_APPS before creating a %s" % (cls.app_label, cls.__name__)

        cls.add_to_class(cls.fkey_name or cls.object_name.lower(),
                         models.ForeignKey('%s.%s' % (cls.app_label, cls.object_name),
                                           related_name='%s_%s_set' % (cls._meta.app_label, cls._meta.module_name),
                                           limit_choices_to = {'calendar_feed__isnull': False}

        ))

    def template_hierarchy(self):
        return ['content/articles/calendar_%s.html' % self.category.slug,
                'content/articles/calendar.html',
               ]
    
