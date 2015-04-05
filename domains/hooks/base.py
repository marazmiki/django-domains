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
    default_value = ''

    def __init__(self, *args, **kwargs):
        self._args = args
        self._kwargs = kwargs
        if self.attribute is None:
            raise ImproperlyConfigured(
                "Please specify `attribute` into  your hook class"
            )

    def __repr__(self):
        v = self.get()
        return text_type(v)

    def __hash__(self):
        return self.get()

    def coerce(self, v):
        return v

    def get(self):
        v = getattr(_thread_locals, self.attribute, self.default_value)
        return self.coerce(v)

    def set(self, value):
        setattr(_thread_locals, self.attribute, self.coerce(value))

    def value(self, request):
        raise NotImplementedError()

    def apply(self, request):
        self.set(self.value(request))


class IntHookBase(HookBase, int):
    default_value = 0

    def coerce(self, v):
        return int(v)

    def __int__(self):
        try:
            return self.get()
        except AttributeError:
            self.set(self.default_value)
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
        return iter(self.get())


class TupleHookBase(HookBase, IterMixin, tuple):
    default_value = ()
    base_type = tuple


class ListHookBase(HookBase, IterMixin, list):
    default_value = []
    base_type = list


class DictHookBase(HookBase, IterMixin, object):
    default_value = {}
    base_type = dict

    def __iter__(self):
        return iter(self.get().items())

    def __getattr__(self, name):
        return self.get()[name]
