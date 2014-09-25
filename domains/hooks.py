# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from domains.utils import _thread_locals


class HookBase(object):
    def __repr__(self):
        return str(self.__int__())

    def __int__(self):
        try:
            return self.get()
        except AttributeError:
            self.set(1)
            return self.get()

    def __hash__(self):
        return self.__int__()

    def get(self):
        return getattr(_thread_locals, self.setting_name)

    def set(self, value):
        setattr(_thread_locals, self.setting_name, value)


class SiteIDHook(HookBase, int):
    """
    Dynamic SITE_ID attribute class
    """
    setting_name = 'SITE_ID'
    settings_type = int


class MediaRootHook(object):
    pass


class MediaUrlHook(object):
    pass


class StaticRootHook(object):
    pass


class StaticUrlHook(object):
    pass