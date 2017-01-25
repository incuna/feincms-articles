#! /usr/bin/env python

from sys import exit


import dj_database_url
import django
from colour_runner.django_runner import ColourRunnerMixin
from django.conf import settings
from django.test.runner import DiscoverRunner


settings.configure(
    ROOT_URLCONF='articles.urls',
    DATABASES={
        'default': dj_database_url.config(
            default='postgres://localhost/articles'
        ),
    },
    INSTALLED_APPS=(
        'articles',
        'tests',

        'feincms',

        'django.contrib.contenttypes',
    ),
    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'APP_DIRS': True,
        }
    ],
)


django.setup()


class TestRunner(ColourRunnerMixin, DiscoverRunner):
    """Enable colorised output."""


test_runner = TestRunner(verbosity=1)
failures = test_runner.run_tests(['tests'])
if failures:
    exit(1)
