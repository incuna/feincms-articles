from distutils.core import setup
setup(
    name = "articles",
    packages = ["articles", ],
    include_package_data=True,
    install_requires=[
        "FeinCMS",
        "django-taggit",
        "django-mptt",
        "django-pagination",
        #"django-denorm",
    ],
    version = "0.1",
    description = "Provides document / articles using (FeinCMS content) with categories and tags.",
    author = "Incuna Ltd",
    author_email = "admin@incuna.com",
    url = "http://incuna.com/",
)
