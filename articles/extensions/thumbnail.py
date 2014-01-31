from django.db import models
from django.utils.translation import ugettext_lazy as _
from feincms import extensions


class Extension(extensions.Extension):
    def handle_model(self):
        self.model.add_to_class(
            'thumbnail',
            models.ImageField(
                _('thumbnail'),
                max_length=250,
                upload_to="images/articles/thumbnails",
                null=True,
                blank=True)
        )

    def handle_modeladmin(self, modeladmin):
        modeladmin.add_extension_options(_('Thumbnail'), {
            'fields': ('thumbnail',),
        })
