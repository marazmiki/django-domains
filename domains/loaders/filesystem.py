# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from django.conf import settings
from django.template.loaders.filesystem import Loader as BaseLoader

from .base import DomainLoaderMixin


class Loader(DomainLoaderMixin, BaseLoader):
    """
    get_template_sources returns the absolute paths to "template_name",
    when appended to each directory in "template_dirs". Any paths that
    don't lie inside one of the template dirs are excluded from the result
    set, for security reasons.
    """
    default_template_dirs = settings.TEMPLATE_DIRS
