# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from django.utils.importlib import import_module


try:
    from django.utils import six
    text_type = six.text_type
except ImportError:
    text_type = str

try:
    from threading import local    # NOQA
except ImportError:
    from django.utils._threading_local import local    # NOQA


try:
    from django.utils.module_loading import import_by_path

except ImportError:
    from django.core.exceptions import ImproperlyConfigured

    def import_by_path(dotted_path, error_prefix=''):
        """
        Import a dotted module path and return the attribute/class
        designated by the last name in the path. Raise ImproperlyConfigured
        if something goes wrong.
        """
        try:
            module_path, class_name = dotted_path.rsplit('.', 1)
        except ValueError:
            raise ImproperlyConfigured(
                "%s%s doesn't look like a module path" % (
                    error_prefix, dotted_path
                )
            )
        try:
            module = import_module(module_path)
        except ImportError as e:
            import sys
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
            raise ImproperlyConfigured(
                '%sModule "%s" does not define a "%s" attribute/class' % (
                    error_prefix, module_path, class_name
                )
            )
        return attr
