from django.db import models
from django.utils.translation import ugettext_lazy as _

def register(cls, admin_cls):
    cls.add_to_class('thumbnail', models.ImageField(_('thumbnail'), max_length=250, upload_to="images/articles/thumbnails", null=True, blank=True))
    if admin_cls:
        admin_cls.add_extension_options(_('Thumbnail'), {
            'fields': ('thumbnail',),
        })


