# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from django.template.loaders.app_directories import Loader as BaseLoader

try:
    # Django 1.7x or older
    from django.template.loaders.app_directories import app_template_dirs

except ImportError:
    # Django 1.8
    from django.template.utils import get_app_template_dirs
    app_template_dirs = get_app_template_dirs('templates')

from .base import DomainLoaderMixin

class Loader(DomainLoaderMixin, BaseLoader):
    """
    get_template_sources looks in the saved request object from the middleware for
    directories and passes back the path. Doesn't verify that the
    path is valid, though.
    """

    default_template_dirs = app_template_dirs
