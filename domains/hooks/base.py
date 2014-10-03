# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from django.core.exceptions import ImproperlyConfigured
from domains.utils import _thread_locals
from domains.compat import text_type


class HookBase(object):
    attribute = None

    def __init__(self, *args, **kwargs):
        self._args = args
        self._kwargs = kwargs
        if self.attribute is None:
            raise ImproperlyConfigured("Please specify `attribute` into "
                                       "your hook class")

    def __repr__(self):
        return text_type(self.get())

    def __hash__(self):
        return self.get()

    def coerce(self, v):
        return v

    def get(self):
        return self.coerce(getattr(_thread_locals, self.attribute))

    def set(self, value):
        setattr(_thread_locals, self.attribute, self.coerce(value))

    def value(self, request):
        raise NotImplementedError()

    def apply(self, request):
        self.set(self.value(request))


class IntHookBase(HookBase, int):
    def coerce(self, v):
        return int(v)

    def __int__(self):
        try:
            return self.get()
        except AttributeError:
            self.set(1)
            return self.get()


class StrHookBase(HookBase, text_type):
    default_value = ''

    def coerce(self, v):
        return text_type(v)

    def __str__(self):
        try:
            return self.get()
        except AttributeError:
            self.set(self.default_value)
            return self.get()

    __unicode__ = __str__


class IterMixin(object):
    def __iter__(self):
        print('%s: %s iter %s' % (self.__class__.__name__,
                                  self.attribute, self.base_type))
        return iter(self.get())

    def coerce(self, v):
        print('%s: %s (%s) coerce to %s' % (self.__class__.__name__,
                                            self.attribute, v,
                                            self.base_type))
        return self.base_type(v)


class TupleHookBase(HookBase, IterMixin, tuple):
    default_value = ()
    base_type = tuple


class ListHookBase(HookBase, IterMixin, list):
    default_value = []
    base_type = list


class DictHookBase(HookBase, IterMixin, dict):
    default_value = {}
    base_type = dict

    def __getitem__(self, key):
        print("getitem")
        return self.get()[key]

    def __setitem__(self, key, value):
        print("setitem")
        v = self.get()
        v.update(**{key: value})
        self.set(v)

    def __delitem__(self, key):
        print("delitem")

        v = self.get()
        del v[key]
        self.set(v)
