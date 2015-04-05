# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from domains.compat import import_by_path, local


# Threaded variable namespace
_thread_locals = local()
installed_hooks = {}


def get_hooks():
    return getattr(
        settings, 'DOMAINS_HOOKS',
        (
            'domains.hooks.site_id.SiteIDHook',
        ))


def setup_hook(hook):
    from domains.hooks.base import HookBase

    hook_cls = import_by_path(hook)
    hook_instance = hook_cls()

    if not isinstance(hook_instance, HookBase):
        raise ImproperlyConfigured(
            '%s is not a HookBase instance' % hook
        )

    installed_hooks[hook_instance.attribute] = hook_instance
    setattr(settings, hook_instance.attribute, hook_instance)


def get_installed_hooks():
    return installed_hooks


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
        return import_by_path(custom_function)(template_dir, template_name)
    hostname = get_hostname()
    return template_dir, hostname, template_name if hostname else None


def get_request():
    """
    Returns request object from current thread
    """
    return get_thread_variable('request')
