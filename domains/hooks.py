# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from domains.utils import _thread_locals


class SiteIDHook(object):
    """
    Dynamic SITE_ID attribute class
    """
    def __repr__(self):
        return str(self.__int__())

    def __int__(self):
        try:
            return _thread_locals.SITE_ID
        except AttributeError:
            _thread_locals.SITE_ID = 1
            return _thread_locals.SITE_ID

    def __hash__(self):
        return self.__int__()

    def set(self, value):
        _thread_locals.SITE_ID = value


class MediaRootHook(object):
    pass


class MediaUrlHook(object):
    pass


class StaticRootHook(object):
    pass


class StaticUrlHook(object):
    pass
