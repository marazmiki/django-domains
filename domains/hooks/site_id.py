# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from django.conf import settings
from django.contrib.sites.models import Site
from django.db.models.loading import get_model
from domains.hooks.base import IntHookBase


HOST_CACHE = {}


def get_site_model():
    """
    Returns Site model
    """
    if 'django.contrib.sites' in settings.INSTALLED_APPS:
        return Site
    if getattr(settings, 'DOMAINS_SITE_MODEL', None):
        return get_model(settings.DOMAIN_SITE_MODEL)
    return None


def get_site_by_host(hostname, field=None):
    site_model = get_site_model()
    field = field or getattr(settings, 'DOMAINS_SITE_FIELD', 'domain')
    try:
        return site_model.objects.get(**{field: hostname})
    except site_model.DoesNotExist:
        pass


class SiteIDHook(IntHookBase):
    """
    Dynamic SITE_ID attribute class
    """
    attribute = 'SITE_ID'
    default_value = 1

    def __init__(self, *args, **kwargs):
        super(IntHookBase, self).__init__(*args, **kwargs)
        self.sites_support = get_site_model() is not None

    def cache(self, host, value):
        HOST_CACHE[host] = value

    def set_and_cache(self, host, site_id):
        self.set(site_id)
        self.cache(host, site_id)

    def apply(self, request):
        if not self.sites_support:
            return
        host = request.get_host()
        shost = host.rsplit(':', 1)[0]  # just host, no port

        if host in HOST_CACHE:
            self.set(HOST_CACHE[host])
            return
        site = get_site_by_host(host)

        if site:
            self.set_and_cache(host, site.pk)
            return

        if shost != host:  # get by hostname without port
            site = get_site_by_host(shost)
            if site:
                self.set_and_cache(host, site.pk)
                return
        site = get_site_by_host(settings.SITE_ID, field='pk')
        if site:
            self.cache(host, site.pk)
            return

        try:  # misconfigured settings?
            site = get_site_model().objects.all()[0]
            self.set_and_cache(host, site.pk)
            return
        except IndexError:  # no sites in db
            pass
