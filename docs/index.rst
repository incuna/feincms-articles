Extensible FeinCMS content article for Django
=============================================

This is an extensible `FeinCMS <https://github.com/feincms/feincms>`_ content
article system for Django, designed to provide a simple Article model that is
extensible.

What is an Article? Many things! You can use it as a news section, as a
knowledge base, as a catalogue of pdfs, or pretty much anything else you can
make it fit with.


Installation and setup
----------------------

Firstly, get the package::

    pip install feincms-articles

You will then need to add ``articles`` to your ``INSTALLED_APPS`` setting::

    INSTALLED_APPS = (
        # ...
        'articles',
    )

Before proceeding with ``manage.py syncdb``, you will need to create some
content types and you may want to add some article extensions. By default the
articles module has a basic set of content fields such as title, summary and
content.


Registering ContentTypes
------------------------

The ``Article`` model extends from :class:`the FeinCMS Base
model <feincms:feincms.models.Base>`, so you need to create some FeinCMS content
types to add to your Articles. No types are created by default, because there
is no way to unregister them. A sane default might be to create
``MediaFileContent`` and ``RichTextContent`` models; you can do this by adding
the following lines somewhere into your project, for example at the bottom of a
``models.py`` file that will be processed anyway::

    from feincms.content.richtext.models import RichTextContent 
    from feincms.content.medialibrary import MediaFileContent

    from articles.models import Article

    Article.register_regions(('top', _('Top content')), ('main', _('Main region')),)

    Article.create_content_type(RichTextContent)
    Article.create_content_type(MediaFileContent, POSITION_CHOICES=(('block', _('block')), ('left', _('left')), ('right', _('right')),))


Extensions
----------

Extensions are a way to add often-used functionality the Article model. The
extensions are standard python modules with a ``register()`` method which will be
called upon registering the extension. The ``register()`` method receives the
``Article`` class itself and the model admin class ``ArticleAdmin`` as arguments.

The extensions can be activated by adding the following to a the bottom of a
``models.py`` file that will be processed anyway::

    from articles.models import Article

    Article.register_extensions(
        'articles.modules.category.extensions.category',
        'feincms.module.extensions.datepublisher',
        'articles.extensions.tags',
        'articles.extensions.thumbnail',
    )

Articles comes with a number of :doc:`bundled extensions<extensions>`, or you
can use the `generic FeinCMS extensions
<http://feincms-django-cms.readthedocs.org/en/latest/api/page.html#extensions-not-specific-to-the-page-module>`_.

.. todo::

    Make this an intersphinx when feincms docs are updated...


Creating your own extensions
----------------------------

To add an extension create a python module that defines a register function
that accepts the ``Article`` class and the ``ArticleAdmin`` class as arguments
and modifies them as required.

Here is the tags extension (similar to articles/extensions/tags.py)::

    def register(cls, admin_cls):
        cls.add_to_class('tags', TaggableManager(verbose_name=_('tags'), blank=True))

        cls.urlpatterns += patterns('taggit.views',
            url(r'^tags/(?P<slug>[^/]+)/$', 'tagged_object_list', {'queryset': cls.objects.active}, name="article_tagged_list"),
        )

        if admin_cls:
            if admin_cls.fieldsets:
                admin_cls.fieldsets[0][1]['fields'].append('tags')


Hooking up articles into your application
-----------------------------------------

You have two main options here, depending on your use case. FeinCMS articles
can be deployed using :ref:`Application content <feincms:integration>`, hooking
up the URLconf ``articles.urls``.

Alternatively you can just use content types to display a list of articles on a
page. There is a bundled content type ``articles.content.ArticleList`` which
will render a fixed number of articles.

If you're not using the FeinCMS page module, the urls and views within articles
are safe to use without ``ApplicationContent``.

The category module also comes with content types for a list of articles
belonging to a certain category
(``articles.modules.category.content.ArticleCategoryList``) and the list of
articles belonging to a set of categories
(``articles.modules.category.content.ArticleList``).

There is also a template tag ``article_tags.articles``, which will render a
list of articles. It takes a optional parameters for ``limit`` (the number of
articles) and the variable to insert the articles list into the context as.


Contents
========

.. toctree::
    :maxdepth: 2

    extensions
    settings


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
