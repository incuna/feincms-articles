Available configuration settings
================================

.. data:: ARTICLE_MODELADMIN_CLASS

    Default: ``django.contrib.admin.ModelAdmin``

    Sets the base class for the ``ModelAdmin`` used by ``Articles``. Note that
    the class will be monkey patched by the extensions.

Specific to the category extension
----------------------------------

.. data:: CATEGORY_MODELADMIN_CLASS

    Default: ``django.contrib.admin.ModelAdmin``

    Sets the base class for the ``ModelAdmin`` used by ``Category``.

.. data:: ARTICLE_SHOW_FIRST_CATEGORY

    Default: ``False``

    When set to ``True``, this will cause the list of Categories view to
    redirect to the first Category's list of articles.

.. data:: ARTICLE_SHOW_DESCENDANTS
    
    Default: ``False``

    When set to ``True``, this will display all articles belonging to any
    descendant category on the list views.
