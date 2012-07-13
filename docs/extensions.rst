Bundled extensions
==================

FeinCMS articles comes with a number of 

.. note::

    Please note that as of FeinCMS 1.6 you will no longer be able to use the
    short-form registration

If the extension requires it's own models (like the category extension) then
the app containing the models will also need to be added to your
``INSTALLED_APPS``.

.. module:: articles.extensions.location

Location extension
------------------

Register: ``articles.extensions.location``.

Requires :mod:`GeoDjango <django:django.contrib.gis>`.

Attaches a physical location point to each article. You will need to ensure you
set :setting:`ARTICLE_MODELADMIN_CLASS` to a (subclass of)
:class:`django:django.contrib.gis.admin.OSMGeoAdmin`

.. module:: articles.extensions.tags

Tags extension
--------------

Register: ``articles.extensions.tags``.

Requires `django-taggit <http://github.com/alex/django-taggit>`_.

Adds tagging to articles. Adds views to the article urls at ``/tags/<tag>/``
to provide a list of articles by tag.

.. module:: articles.extensions.thumbnails

Thumbnail extension
-------------------

Register: ``articles.extensions.thumbnail``.

Adds a simple ``ImageField`` for use as an article thumbnail. Requires PIL, but
you knew that already right?

.. module:: articles.modules.category.extensions.category

Category extension
------------------

Register: ``articles.modules.category.extensions.category``.

Requires the category module to be added to installed apps::

    INSTALLED_APPS = (
        ...
        'articles.modules.category',
    )

This is a nested category setup, that is categories can live within other
categories. The extension will update the url structure of ``articles.urls`` to
reflect the new structure.
