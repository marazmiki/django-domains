# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from django.conf.urls import url
from django.shortcuts import render


urlpatterns = [
    url('^$', lambda request: render(request, 'test_index.html')),
]
