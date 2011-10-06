from setuptools import setup, find_packages

from articles import get_version

setup(
    name = "feincms-articles",
    packages = find_packages(),
    include_package_data=True,
    install_requires=[
        "FeinCMS",
        "django-mptt",
        "django-pagination",
    ],
    version = get_version(),
    description = "Provides Articles using (FeinCMS content) with categories and tags.",
    author = "Incuna Ltd",
    author_email = "admin@incuna.com",
    url = "https://bitbucket.org/incuna/feincms-articles/",
)
