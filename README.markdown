Extensible FeinCMS content article for Django
============================================

This is an extensible FeinCMS content article system for Django, designed to
provide a simple Article model that is extensible. The concept (and some code)
is borrowed from the [FeinCMS](https://github.com/matthiask/feincms) Page
model.

Installation and setup
----------------------

Firstly, get the package.

    pip install feincms-articles

You will then need to add `articles` to your `INSTALLED_APPS` setting.

Before proceeding with `manage.py syncdb`, you may want to add some article
extensions. By default the articles module has a basic set of content fields
such as title, summary and content.

Extensions
----------

Extensions are a way to add often-used functionality the Article model. The
extensions are standard python modules with a `register()` method which will be
called upon registering the extension. The `register()` method receives the
`Article` class itself and the model admin class `ArticleAdmin` as arguments. 

The extensions can be activated by adding the following to a the bottom of a
`models.py` file that will be processed anyway:

    from articles.models import Article
    Article.register_extensions('articles.modules.category.extensions.category', 'datepublisher', 'tags', 'thumbnail') 

If the extension requires it's own models (like the category extension) then
the app containing the models will also need to be added to your
`INSTALLED_APPS`.


ContentTypes
------------

You need to create some FeinCMS content types to add to your Articles. No
models are created by default, because there is no way to unregister
models. A sane default might be to create `ImageContent` and `RichTextContent`
models; you can do this by adding the following lines somewhere into your
project, for example at the bottom of a `models.py` file that will be processed
anyway:

    from feincms.content.richtext.models import RichTextContent 
    from feincms.content.image.models import ImageContent

    from articles.models import Article

    Article.register_regions(('top', _('Top content')), ('main', _('Main region')),)

    Article.create_content_type(RichTextContent)
    Article.create_content_type(ImageContent, POSITION_CHOICES=(('block', _('block')), ('left', _('left')), ('right', _('right')),))


Adding extensions
-----------------

To add an extension create a python module that defines a register function
that accepts the Article class and the ArticleAdmin class as arguments and
modifies them as required.

Here is the address extension (profiles/extensions/tags.py):

    def register(cls, admin_cls):
        cls.add_to_class('tags', TaggableManager(verbose_name=_('tags'), blank=True))

        cls.urlpatterns += patterns('taggit.views',
            url(r'^tags/(?P<slug>[^/]+)/$', 'tagged_object_list', {'queryset': cls.objects.active}, name="article_tagged_list"),
        )

        if admin_cls:
            if admin_cls.fieldsets:
                admin_cls.fieldsets[0][1]['fields'].append('tags')

