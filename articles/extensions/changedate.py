from datetime import datetime
from django.db import models
from django.utils.translation import ugettext_lazy as _


def register(cls, admin_cls):
    cls.add_to_class('creation_date', models.DateTimeField(_('creation date'), blank=True, null=True, editable=False, default=datetime.now))
    cls.add_to_class('modification_date', models.DateTimeField(_('modification date'), auto_now=True))
