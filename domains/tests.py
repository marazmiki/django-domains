# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from django import test, get_version
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings
from django.conf.urls import url
from django.contrib.sites.models import Site
from django.shortcuts import render
from domains import setup_hook
from domains.compat import text_type
from domains.hooks.base import (StrHookBase, TupleHookBase, ListHookBase,
                                DictHookBase, IntHookBase)


urlpatterns = [
    url('^$', lambda request: render(request, 'test_index.html')),
]


def hook_str(h):
    return h


def hook_int(h):
    return len(h)


def hook_dict(h):
    return {1: h + '_1', 2: h + '_2'}


def hook_list(h):
    return [h, h, h]


def hook_tuple(h):
    return (h, h, h)


def test_function(template_dir, template_name):
    """
    Generates parts of template name
    """
    return template_dir, 'custom_' + template_name


class TestHookBase(object):
    hook_function = hook_str

    def value(self, request):
        return globals()[self.hook_function](request.get_host())


class TestIntHook(TestHookBase, IntHookBase):
    """
    Test cases for integer variables hook
    """
    attribute = 'DOMAINS_TEST_ATTRIBUTE_INT'
    hook_function = 'hook_int'


class TestStrHook(TestHookBase, StrHookBase):
    """
    Test cases for string variables hook
    """
    attribute = 'DOMAINS_TEST_ATTRIBUTE_STR'
    hook_function = 'hook_str'


class TestDictHook(TestHookBase, DictHookBase):
    """
    Test cases for dictionary variables hook
    """
    attribute = 'DOMAINS_TEST_ATTRIBUTE_DICT'
    hook_function = 'hook_dict'


class TestListHook(TestHookBase, ListHookBase):
    """
    Test cases for list variables hook
    """
    attribute = 'DOMAINS_TEST_ATTRIBUTE_LIST'
    hook_function = 'hook_list'


class TestTupleHook(TestHookBase, TupleHookBase):
    """
    Test cases for tuple variables hook
    """
    attribute = 'DOMAINS_TEST_ATTRIBUTE_TUPLE'
    hook_function = 'hook_tuple'


class EnvironmentTest(test.TestCase):
    """
    Tests the environment
    """
    def test_middleware(self):
        self.assertIn(
            'domains.middleware.RequestMiddleware',
            settings.MIDDLEWARE_CLASSES
        )


class TestBase(test.TestCase):
    """
    Common things
    """
    urls = 'domains.tests'

    def setUp(self):
        """
        Runs before each unit test
        """
        self.client = test.Client()


class TemplateLoadersTest(TestBase):
    """
    Test suite for dynamic template directories
    """

    def test_foo_dot_com(self):
        """
        Tests for first domain
        """
        resp = self.client.get('/', HTTP_HOST='test.foo.com')
        self.assertContains(resp, text='test.foo.com')
        self.assertNotContains(resp, text='test.bar.com')

    def test_bar_dot_com(self):
        """
        Tests for second domain
        """
        resp = self.client.get('/', HTTP_HOST='test.bar.com')
        self.assertContains(resp, 'test.bar.com')
        self.assertNotContains(resp, 'test.foo.com')

    def test_another_domain(self):
        """
        Tests if templates with domain name not found
        """
        resp = self.client.get('/', HTTP_HOST='github.com')
        self.assertNotContains(resp, 'test.bar.com')
        self.assertNotContains(resp, 'test.foo.com')
        self.assertContains(resp, 'DEFAULT')

    def test_complex(self):
        """
        Complex
        """
        tests = (
            ('test.foo.com', 'test.foo.com'),
            ('microsoft.com', 'DEFAULT'),
            ('test.foo.com', 'test.foo.com'),
            ('test.bar.com', 'test.bar.com'),
            ('google.com', 'DEFAULT'),
            ('test.bar.com', 'test.bar.com'),
            ('test.foo.com', 'test.foo.com'),
            ('yahoo.com', 'DEFAULT'),
        )

        for domain, content in tests:
            resp = self.client.get('/', HTTP_HOST=domain)
            self.assertContains(resp, content)

    def test_custom_function(self):
        """
        Custom function
        """
        func = 'domains.tests.test_function'
        with self.settings(DOMAINS_TEMPLATE_NAME_FUNCTION=func):
            resp = self.client.get('/', HTTP_HOST='microsoft.com')
            self.assertContains(resp, 'CUSTOM')

    def test_hook_str(self):
        domain = 'test.foo.com'
        self.client.get('/', HTTP_HOST=domain)
        self.assertEquals(hook_str(domain),
                          text_type(settings.DOMAINS_TEST_ATTRIBUTE_STR))

    def test_hook_int(self):
        domain = 'test.foo.com'
        self.client.get('/', HTTP_HOST=domain)
        self.assertEquals(hook_int(domain),
                          int(settings.DOMAINS_TEST_ATTRIBUTE_INT))

    def test_hook_tuple(self):
        domain = 'test.foo.com'
        self.client.get('/', HTTP_HOST=domain)
        self.assertEquals(hook_tuple(domain),
                          tuple(settings.DOMAINS_TEST_ATTRIBUTE_TUPLE))

    def test_hook_list(self):
        domain = 'test.foo.com'
        self.client.get('/', HTTP_HOST=domain)
        self.assertEquals(hook_list(domain),
                          list(settings.DOMAINS_TEST_ATTRIBUTE_LIST))

    def test_hook_dict(self):
        domain = 'test.foo.com'
        self.client.get('/', HTTP_HOST=domain)
        self.assertDictEqual(hook_dict(domain),
                             dict(settings.DOMAINS_TEST_ATTRIBUTE_DICT))


class SiteIdTest(TestBase):
    """
    Test dynamic
    """
    def setUp(self):
        super(SiteIdTest, self).setUp()
        self.sites = {
            1: Site.objects.create(domain='test.foo.com', name='Foo'),
            2: Site.objects.create(domain='test.bar.com', name='Bar'),
            3: Site.objects.create(domain='github.com', name='Git'),
        }

    def test_1(self):
        for _ in range(0, 3):
            for pk, site in self.sites.items():
                resp = self.client.get('/', HTTP_HOST=site.domain)

                if get_version() >= '1.8':
                    curr = Site.objects.get_current(resp.context['request'])
                else:
                    curr = Site.objects.get_current()

                self.assertEquals(curr.domain, site.domain)
                self.assertEquals(curr.pk, site.pk)


class TestCore(test.TestCase):
    def test_improperly_hook_class(self):
        self.assertRaises(ImproperlyConfigured,
                          lambda: setup_hook('hook.that.DoesNotExist'))
