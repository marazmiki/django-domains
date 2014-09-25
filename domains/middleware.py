# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from django.conf import settings
from domains.settings import HOOKS
from domains.utils import (set_thread_variable, get_site_by_host,
                           get_site_model, get_hooks, apply_hook)
import warnings


HOST_CACHE = {}


class RequestMiddleware(object):
    """
    Stores the request object in the local thread
    """
    def process_request(self, request):
        set_thread_variable('request', request)


class DomainSettingsPatchMiddleware(object):
    def __init__(self):
        self.sites_support = get_site_model() is not None

    def process_request(self, request):
        for hook in get_hooks():
            apply_hook(hook, request=request)


class DynamicSiteMiddleware(DomainSettingsPatchMiddleware):
    """
    Define current Django Site for requested hostname
    """

    def __init__(self):
        super(DynamicSiteMiddleware, self).__init__()
        warnings.warn("DynamicSiteMiddleware is deprecated. Please use "
                      "DomainSettingsPatchMiddleware instead")

    def patch_site_id(self, request):
        host = request.get_host()
        shost = host.rsplit(':', 1)[0]  # just host, no port

        if host in HOST_CACHE:
            settings.SITE_ID.set(HOST_CACHE[host])
            return

        site = get_site_by_host(host)

        if site:
            HOST_CACHE[host] = site.pk
            settings.SITE_ID.set(site.pk)

        if shost != host:  # get by hostname without port
            site = get_site_by_host(shost)
            if site:
                HOST_CACHE[host] = site.pk
                settings.SITE_ID.set(site.pk)
                return

        site = get_site_by_host(settings.SITE_ID, field='pk')
        if site:
            HOST_CACHE[host] = site.pk
            return

        try:  # misconfigured settings?
            site = get_site_model().objects.all()[0]
            HOST_CACHE[host] = site.pk
            settings.SITE_ID.set(site.pk)
            return
        except IndexError:  # no sites in db
            pass
