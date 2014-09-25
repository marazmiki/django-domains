# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from django.conf import settings
from django.utils.importlib import import_module

try:
    from threading import local
except ImportError:
    from django.utils._threading_local import local


try:
    from django.utils.module_loading import import_by_path
except ImportError:
    from django.core.exceptions import ImproperlyConfigured

    def import_by_path(dotted_path, error_prefix=''):
        """
        Import a dotted module path and return the attribute/class designated by the
        last name in the path. Raise ImproperlyConfigured if something goes wrong.
        """
        try:
            module_path, class_name = dotted_path.rsplit('.', 1)
        except ValueError:
            raise ImproperlyConfigured("%s%s doesn't look like a module path" % (
                                       error_prefix, dotted_path))
        try:
            module = import_module(module_path)
        except ImportError as e:
            msg = '%sError importing module %s: "%s"' % (
                error_prefix, module_path, e)
            try:
                from django.utils import six
                six.reraise(ImproperlyConfigured, ImproperlyConfigured(msg),
                            sys.exc_info()[2])
            except ImportError:
                raise ImproperlyConfigured(msg)
        try:
            attr = getattr(module, class_name)
        except AttributeError:
            raise ImproperlyConfigured('%sModule "%s" does not define a "%s" attribute/class' % (
                error_prefix, module_path, class_name))
        return attr


# Threaded variable namespace
_thread_locals = local()


def get_hooks():
    return getattr(
        settings, 'DOMAINS_HOOKS',
        (
            ('SITE_ID', 'domains.hooks.SiteIDHook'),
        ))


def get_site_model():
    if 'django.contrib.sites' in settings.INSTALLED_APPS:
        from django.contrib.sites.models import Site
        return Site
    if getattr(settings, 'DOMAINS_SITE_MODEL', None):
        from django.db.models.loading import get_model
        return get_model(settings.DOMAIN_SITE_MODEL)

def get_site_by_host(hostname, field=None):
    Site = get_site_model()
    field = field or getattr(settings, 'DOMAINS_SITE_FIELD', 'domain')

    try:
        return Site.objects.get(**{field: hostname})
    except Site.DoesNotExist:
        pass


def apply_hook(hook, attribute, request):
    c = import_by_path(hook)

def set_hook(hook):
    hook_cls = import_by_path(hook)
    hook_instance = hook_cls()
    setattr(settings, hook_instance.attribute, hook_instance)

def set_thread_variable(key, var):
    """
    Sets the threaded variable
    """
    setattr(_thread_locals, key, var)


def get_thread_variable(key, default=None):
    """
    Gets the threaded variable
    """
    return getattr(_thread_locals, key, default)


def get_hostname():
    """
    Returns the current domain name in lower case and without port number
    """
    request = get_request()
    if request is None:
        return
    return request.get_host().split(':')[0].lower()


def get_template_name(template_dir, template_name):
    """
    Generates parts of template name
    """
    custom_function = getattr(settings, 'DOMAINS_TEMPLATE_NAME_FUNCTION', None)

    if custom_function is not None:
        module, func = custom_function.rsplit('.', 1)
        return getattr(import_module(module), func)(template_dir,
                                                    template_name)
    hostname = get_hostname()
    return template_dir, hostname, template_name if hostname else None


def get_request():
    """
    Returns request object from current thread
    """
    return get_thread_variable('request')
