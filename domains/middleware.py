# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from domains.utils import set_thread_variable, get_installed_hooks
import warnings


class RequestMiddleware(object):
    """
    Stores the request object in the local thread
    """
    def process_request(self, request):
        set_thread_variable('request', request)


class DomainSettingsPatchMiddleware(object):
    def process_request(self, request):
        for attr, hook in get_installed_hooks().items():
            hook.apply(request)


class DynamicSiteMiddleware(DomainSettingsPatchMiddleware):
    """
    Define current Django Site for requested hostname
    """
    def __init__(self):
        super(DynamicSiteMiddleware, self).__init__()
        warnings.warn(
            "domains.middleware.DynamicSiteMiddleware is deprecated. "
            "Please use domains.middleware.DomainSettingsPatchMiddleware "
            "instead"
        )
