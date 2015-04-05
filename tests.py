#!/usr/bin/env python
# coding: utf-8

from django.conf import settings
from django import get_version
import sys
import os


sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))


TEST_RUNNER = 'django.test.simple.DjangoTestSuiteRunner'

if get_version() >= '1.6':
    TEST_RUNNER = 'django.test.runner.DiscoverRunner'


SETTINGS = dict(
    SITE_ID=1,
    TEST_RUNNER=TEST_RUNNER,
    DEBUG=False,
    ROOT_URLCONF='domains.tests.urls',
    INSTALLED_APPS=(
        'django.contrib.sessions',
        'django.contrib.sites',
        'domains',
    ),
    MIDDLEWARE_CLASSES=(
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'domains.middleware.RequestMiddleware',
        'domains.middleware.DynamicSiteMiddleware',
    ),
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':MEMORY:'
        }
    },
    DOMAINS_TEST_ATTRIBUTE_STR='default',
    DOMAINS_TEST_ATTRIBUTE_INT=42,
    DOMAINS_TEST_ATTRIBUTE_DICT={1: 1, 2: 2},
    DOMAINS_TEST_ATTRIBUTE_LIST=[1, 2, 3],
    DOMAINS_TEST_ATTRIBUTE_TUPLE=('one', 'two'),
    DOMAINS_HOOKS=(
        'domains.hooks.site_id.SiteIDHook',
        'domains.tests.TestStrHook',
        'domains.tests.TestIntHook',
        'domains.tests.TestListHook',
        'domains.tests.TestDictHook',
        'domains.tests.TestTupleHook',
    ))


TEMPLATE_LOADERS = (
    'domains.loaders.filesystem.Loader',
    'domains.loaders.app_directories.Loader',
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)


TEMPLATE_CONTEXT_PROCESSORS = (
    'django.template.context_processors.request',
)

if get_version() >= '1.8':
    SETTINGS['TEMPLATES'] = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'OPTIONS': {
                'loaders': TEMPLATE_LOADERS,
                'context_processors': TEMPLATE_CONTEXT_PROCESSORS,
            },
        }]

else:
    SETTINGS.update(TEMPLATE_LOADERS=TEMPLATE_LOADERS)


settings.configure(**SETTINGS)


def main():
    from django.test.utils import get_runner
    import django

    if hasattr(django, 'setup'):
        django.setup()

    find_pattern = 'domains'

    test_runner = get_runner(settings)(verbosity=2, interactive=True)
    failed = test_runner.run_tests([find_pattern])
    sys.exit(failed)


if __name__ == '__main__':
    main()
