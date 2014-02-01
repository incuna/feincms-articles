"""Inspired by http://stackoverflow.com/a/12260597/400691"""
import sys

from django.conf import settings

import dj_database_url


settings.configure(
    DATABASES={
        'default': dj_database_url.config(default='postgres://localhost/feincms_articles'),
    },
    INSTALLED_APPS=(
        'articles',
        'articles.tests',

        'feincms',
        'taggit',
        # Put contenttypes before auth to work around test issue.
        # See: https://code.djangoproject.com/ticket/10827#comment:12
        'django.contrib.contenttypes',
        'django.contrib.auth',
        'django.contrib.sessions',
        'django.contrib.admin',
    ),
    PASSWORD_HASHERS = ('django.contrib.auth.hashers.MD5PasswordHasher',),
    #AUTH_USER_MODEL='tests.User',
    ROOT_URLCONF='articles.urls',
)

from django.test.runner import DiscoverRunner

test_runner = DiscoverRunner(verbosity=1)
failures = test_runner.run_tests(['articles'])
if failures:
    sys.exit(1)
