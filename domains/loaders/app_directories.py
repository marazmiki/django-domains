# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from django.template.loaders.app_directories import Loader as BaseLoader
from django.utils._os import safe_join
from domains.utils import get_template_name


try:
    from django.template.loaders.app_directories import app_template_dirs

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

except ImportError:
    # The new Django 1.8 template API
    from django.template.utils import get_app_template_dirs
    from django.core.exceptions import SuspiciousFileOperation
    from django.template.base import TemplateDoesNotExist
    import io

    app_template_dirs = get_app_template_dirs('templates')

    class Loader(BaseLoader):
        is_usable = True

        def get_template_sources(self, template_name, template_dirs=None):
            """
            Returns the absolute paths to "template_name", when appended to each
            directory in "template_dirs". Any paths that don't lie inside one of the
            template dirs are excluded from the result set, for security reasons.
            """
            if not template_dirs:
                template_dirs = get_app_template_dirs('templates')

            for template_dir in template_dirs:
                try:
                    template_parts = get_template_name(template_dir, template_name)

                    if not template_parts:
                        continue
                    yield safe_join(*template_parts)
                except SuspiciousFileOperation:
                    # The joined path was located outside of this template_dir
                    # (it might be inside another one, so this isn't fatal).
                    pass

        def load_template_source(self, template_name, template_dirs=None):
            for filepath in self.get_template_sources(template_name, template_dirs):
                try:
                    with io.open(filepath, encoding=self.engine.file_charset) as fp:
                        return fp.read(), filepath
                except IOError:
                    pass
            raise TemplateDoesNotExist(template_name)
