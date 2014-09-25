# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from domains.utils import _thread_locals


class HookBase(object):
    attribute = 'DJANGO_ATTRIBUTE'

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
        return getattr(_thread_locals, self.attribute)

    def set(self, value):
        setattr(_thread_locals, self.attribute, value)

    def apply(self, request):
        raise NotImplementedError()
