from django import test
from django.conf import settings
from django.contrib.sites.models import Site

class EnvironmentTest(test.TestCase):
    """
    Tests the environment
    """
    def test_middleware(self):
        self.assertTrue('domains.middleware.RequestMiddleware' in settings.MIDDLEWARE_CLASSES)

class TestBase(test.TestCase):
    """
    Common things
    """
    urls = 'domains.tests.urls'

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
        assert 'test.foo.com' in resp.content
        assert 'test.bar.com' not in resp.content

    def test_bar_dot_com(self):
        """
        Tests for second domain
        """
        resp = self.client.get('/', HTTP_HOST='test.bar.com')
        assert 'test.bar.com' in resp.content
        assert 'test.foo.com' not in resp.content

    def test_another_domain(self):
        """
        Tests if templates with domain name not found
        """
        resp = self.client.get('/', HTTP_HOST='github.com')
        assert 'test.bar.com' not in resp.content
        assert 'test.foo.com' not in resp.content
        assert 'DEFAULT' in resp.content

    def test_complex(self):
        """
        Complex
        """
        tests = (
            ('test.foo.com',   'test.foo.com'),
            ('microsoft.com',  'DEFAULT'),
            ('test.foo.com',   'test.foo.com'),
            ('test.bar.com',   'test.bar.com'),
            ('google.com',     'DEFAULT'),
            ('test.bar.com',   'test.bar.com'),
            ('test.foo.com',   'test.foo.com'),
            ('yahoo.com',      'DEFAULT'),
        )

        for domain, content in tests:
            resp = self.client.get('/', HTTP_HOST=domain)
            self.assertEquals(content, resp.content)

    def test_custom_function(self):
        """
        Custom function
        """
        setattr(settings, 'DOMAINS_TEMPLATE_NAME_FUNCTION', 'domains.tests.test_function')
        resp = self.client.get('/', HTTP_HOST='microsoft.com')

        try:
            self.assertEquals('CUSTOM', resp.content)
            delattr(settings, 'DOMAINS_TEMPLATE_NAME_FUNCTION')
        except:
            # Test failing shall not affect to other cases
            delattr(settings, 'DOMAINS_TEMPLATE_NAME_FUNCTION')
            raise

class SiteIdTest(TestBase):
    """
    Test dynamic
    """
    def setUp(self):
        super(SiteIdTest, self).setUp()
        self.sites = {
            1: Site.objects.create(domain='test.foo.com', name='Foo'),
            2: Site.objects.create(domain='test.bar.com', name='Bar'),
            3: Site.objects.create(domain='github.com',   name='Git'),
        }

    def test_1(self):
        for i in xrange(0, 3):
            for pk, site in self.sites.items():
                resp = self.client.get('/', HTTP_HOST=site.domain)
                curr = Site.objects.get_current()
                self.assertEquals(curr.domain, site.domain)
                self.assertEquals(curr.pk,     site.pk)

def test_function(template_dir, template_name):
    """
    Generates parts of template name
    """
    return template_dir, 'custom_'+template_name
