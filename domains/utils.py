from django.conf import settings
from django.utils.importlib import import_module

try:
    from threading import local
except ImportError:
    from django.utils._threading_local import local

# Threaded variable namespace
_thread_locals = local()

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

class SiteIDHook(object):
    """
    Dynamic SITE_ID attribute class
    """
    def __repr__(self):
        return str(self.__int__())

    def __int__(self):
        try:
            return _thread_locals.SITE_ID
        except AttributeError:
            _thread_locals.SITE_ID = 1
            return _thread_locals.SITE_ID

    def __hash__(self):
        return self.__int__()

    def set(self, value):
        _thread_locals.SITE_ID = value
