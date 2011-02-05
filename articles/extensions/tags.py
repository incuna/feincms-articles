from django.utils.translation import ugettext_lazy as _
from tagging.fields import TagField

def register(cls, admin_cls):
    cls.add_to_class('tags', TagField(_('tags'), null=True, blank=True))
    if admin_cls:
        if admin_cls.fieldsets:
            admin_cls.fieldsets[0][1]['fields'].append('tags')

