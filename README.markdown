Extensible FeinCMS content article for Django
=============================================

This is an extensible [FeinCMS](https://github.com/feincms/feincms) content
article system for Django, designed to provide a simple Article model that is
extensible.

What is an Article? Many things! You can use it as a news section, as a
knowledge base, as a catalogue of pdfs, or pretty much anything else you can
make it fit with.

Full documentation at http://feincms-articles.rtfd.org


Installation and setup
----------------------

Firstly, get the package.

    pip install feincms-articles

You will then need to add `articles` to your `INSTALLED_APPS` setting:

    INSTALLED_APPS = (
        # ...
        'articles',
    )

Before proceeding with `manage.py syncdb`, you will need to create some content
types and you may want to add some article extensions. By default the articles
module has a basic set of content fields such as title, summary and content.


ContentTypes
------------

You need to create some FeinCMS content types to add to your Articles. No types
are created by default, because there is no way to unregister them. A sane
default might be to create `MediaFileContent` and `RichTextContent` models; you
can do this by adding the following lines somewhere into your project, for
example at the bottom of a `models.py` file that will be processed anyway:

    from feincms.content.richtext.models import RichTextContent 
    from feincms.content.medialibrary.v2 import MediaFileContent

    from articles.models import Article

    Article.register_regions(('top', _('Top content')), ('main', _('Main region')),)

    Article.create_content_type(RichTextContent)
    Article.create_content_type(MediaFileContent, TYPE_CHOICES=(('block', _('block')), ('left', _('left')), ('right', _('right')),))


Extensions
----------

Extensions are a way to add often-used functionality the Article model. The
extensions are standard python modules with a `register()` method which will be
called upon registering the extension. The `register()` method receives the
`Article` class itself and the model admin class `ArticleAdmin` as arguments. 

The extensions can be activated by adding the following to a the bottom of a
`models.py` file that will be processed anyway:

    from articles.models import Article

    Article.register_extensions(
        'articles.modules.category.extensions.category',
        'feincms.module.extensions.datepublisher',
        'articles.extensions.tags',
        'articles.extensions.thumbnail',
    )

If the extension requires it's own models (like the category extension) then
the app containing the models will also need to be added to your
`INSTALLED_APPS`.

List of available extensions:

- `articles.extensions.location`
- `articles.extensions.tags`
- `articles.extensions.thumbnails`
- `articles.modules.category.extensions.category`

You can also use some of the generic extensions from
[FeinCMS](https://github.com/feincms/feincms/tree/master/feincms/module/extensions).



Creating your own extensions
----------------------------

To add an extension create a python module that defines a register function
that accepts the Article class and the ArticleAdmin class as arguments and
modifies them as required.

Here is the address extension (similar to articles/extensions/tags.py):

    def register(cls, admin_cls):
        cls.add_to_class('tags', TaggableManager(verbose_name=_('tags'), blank=True))

        cls.urlpatterns += [
            url(r'^tags/(?P<slug>[^/]+)/$', 'taggit.views.tagged_object_list', {'queryset': cls.objects.active}, name="article_tagged_list"),
        ]

        if admin_cls:
            if admin_cls.fieldsets:
                admin_cls.fieldsets[0][1]['fields'].append('tags')
