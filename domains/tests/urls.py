from django.conf.urls.defaults import *
from django.shortcuts import render

def index(request):
    return render(request, 'test_index.html', {})

urlpatterns = patterns('',
    url('^$', index),
)