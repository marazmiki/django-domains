# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from django.core.exceptions import SuspiciousFileOperation
try:
    from django.template import Origin
except ImportError:
    Origin = None
from django.utils._os import safe_join
from domains.utils import get_template_name


class DomainLoaderMixin(object):
    is_usable = True

    def get_template_sources(self, template_name, template_dirs=None):
        """
        Returns the absolute paths to "template_name", when appended to each
        directory in "template_dirs". Any paths that don't lie inside one of
        the template dirs are excluded from the result set, for
        security reasons.
        """
        if not template_dirs:
            template_dirs = self.default_template_dirs

        try:
            use_origin = self.get_contents is not None
        except AttributeError:
            use_origin = False

        for template_dir in template_dirs:
            try:
                template_parts = get_template_name(template_dir, template_name)
                if not template_parts:
                    continue
                name = safe_join(*template_parts)

                if use_origin:
                    yield Origin(
                        name=name,
                        template_name=template_name,
                        loader=self,
                    )
                else:
                    yield name

            except UnicodeDecodeError:
                # The template dir name was a bytestring that
                # wasn't valid UTF-8.
                raise
            except SuspiciousFileOperation:
                # The joined path was located outside of this particular
                # template_dir (it might be inside another one, so this isn't
                # fatal).
                pass
