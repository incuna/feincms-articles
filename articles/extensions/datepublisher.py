"""
Allows setting a date range for when the article is active. Modifies the active()
manager method so that only pages inside the given range.
"""

from datetime import datetime

from django.db import models
from django.db.models import Q
from django.conf import settings
from django.utils.dateformat import format
from django.utils.translation import ugettext_lazy as _

def format_date(d, if_none=''):
    """
    Format a date in a nice human readable way: Omit the year if it's the current
    year. Also return a default value if no date is passed in.
    """

    if d is None: return if_none

    fmt = settings.SHORT_DATETIME_FORMAT
    return format(d, fmt)


def register(cls, admin_cls):
    cls.add_to_class('publication_date', models.DateTimeField(_('publication date'), default=datetime.now,))
    cls.add_to_class('publication_end_date', models.DateTimeField(_('publication end date'), null=True, blank=True,
                                                                  help_text=_('Leave empty if the entry should stay active forever.')))


    cls._meta.ordering.insert(0, '-publication_date')
    cls._meta.get_latest_by = 'publication_date'

    cls.objects.active_filters['date'] = (Q(publication_date__lte=datetime.now) &
        (Q(publication_end_date__isnull=True) | Q(publication_end_date__gt=datetime.now)))

    if admin_cls:
        def datepublisher_admin(self, page):
            return u'%s &ndash; %s' % (
                format_date(page.publication_date),
                format_date(page.publication_end_date, '&infin;'),
                )
        datepublisher_admin.allow_tags = True
        datepublisher_admin.short_description = _('visible from - to')

        admin_cls.datepublisher_admin = datepublisher_admin
        admin_cls.list_display.insert(admin_cls.list_display.index('active') + 1, 'datepublisher_admin')
        admin_cls.date_hierarchy = 'publication_date'

        if admin_cls.fieldsets:
            fields = admin_cls.fieldsets[0][1]['fields']
            fields += ['publication_date', 'publication_end_date']
