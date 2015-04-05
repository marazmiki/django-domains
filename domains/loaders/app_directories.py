# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from django.template.loaders.app_directories import Loader as BaseLoader
from django.utils._os import safe_join
from domains.utils import get_template_name


try:
    # Django 1.7x or older
    from django.template.loaders.app_directories import app_template_dirs

except ImportError:
    # Django 1.8
    from django.template.utils import get_app_template_dirs
    app_template_dirs = get_app_template_dirs('templates')


class Loader(BaseLoader):
    is_usable = True

    def get_template_sources(self, template_name, template_dirs=None):
        """
        Looks in the saved request object from the middleware for
        directories and passes back the path. Doesn't verify that the
        path is valid, though.
        """
        if not template_dirs:
            template_dirs = app_template_dirs

        for template_dir in template_dirs:
            try:
                template_parts = get_template_name(template_dir, template_name)
                if not template_parts:
                    continue
                yield safe_join(*template_parts)
            except UnicodeDecodeError:
                # The template dir name was a bytestring
                # that wasn't valid UTF-8.
                raise
            except ValueError:
                # The joined path was located outside of template_dir.
                pass
