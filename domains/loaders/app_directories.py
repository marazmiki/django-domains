from django.template.loaders.app_directories import Loader as BaseLoader, app_template_dirs
from django.conf import settings
from django.utils._os import safe_join
from domains.utils import get_template_name
import os

class Loader(BaseLoader):
    """
    Django 1.2 version of the template loader class
    """
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
                # The template dir name was a bytestring that wasn't valid UTF-8.
                raise
            except ValueError:
                # The joined path was located outside of template_dir.
                pass
