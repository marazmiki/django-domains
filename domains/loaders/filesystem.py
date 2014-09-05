# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from django.conf import settings
from django.template.loaders.filesystem import Loader as BaseLoader
from django.utils._os import safe_join
from domains.utils import get_template_name


class Loader(BaseLoader):
    is_usable = True

    def get_template_sources(self, template_name, template_dirs=None):
        """
        Returns the absolute paths to "template_name", when appended to each
        directory in "template_dirs". Any paths that don't lie inside one of
        the template dirs are excluded from the result set, for
        security reasons.
        """
        if not template_dirs:
            template_dirs = settings.TEMPLATE_DIRS

        for template_dir in template_dirs:
            try:
                template_parts = get_template_name(template_dir, template_name)
                if not template_parts:
                    continue
                yield safe_join(*template_parts)

            except UnicodeDecodeError:
                # The template dir name was a bytestring that
                # wasn't valid UTF-8.
                raise
            except ValueError:
                # The joined path was located outside of this particular
                # template_dir (it might be inside another one, so this isn't
                # fatal).
                pass
