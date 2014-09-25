# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from django.contrib.staticfiles.finders import BaseFinder
from django.contrib.staticfiles.storage import AppStaticStorage
from django.contrib.staticfiles import utils
from django.utils.datastructures import SortedDict
from django.utils.importlib import import_module
from django.conf import settings
from .middleware import get_current_request, get_active_layer
import os


class LayerStaticStorage(AppStaticStorage):
    def __init__(self, app, layer, *args, **kwargs):
        """
        Returns a static file storage if available in the given app.
        """
        # app is the actual app module
        self.layer = layer
        mod = import_module(app)
        mod_path = os.path.dirname(mod.__file__)
        location = os.path.join(mod_path, "layers", layer, 'static')
        super(AppStaticStorage, self).__init__(location, *args, **kwargs)


class AppLayerFinder(BaseFinder):
    storage_class = LayerStaticStorage

    def __init__(self, apps=None, *args, **kwargs):
        layers = getattr(settings, "LAYERS", {})
        self.apps = []
        self.storages = SortedDict()
        if apps is None:
            apps = settings.INSTALLED_APPS
        for app in apps:
            for layer in layers.keys():
                app_storage = self.storage_class(app, layer)
                if os.path.isdir(app_storage.location):
                    if app not in self.apps:
                        self.apps.append(app)
                    if app not in self.storages:
                        self.storages[app] = {}

                    self.storages[app][layer] = app_storage
        super(AppLayerFinder, self).__init__(*args, **kwargs)

    def find(self, path, all=False, layer=None):
        """
        Looks for files in the app directories.
        """
        matches = []
        for app in self.apps:
            match = self.find_in_app(app, path, layer)
            if match:
                if not all:
                    return match
                matches.append(match)
        return matches

    def find_in_app(self, app, path, layer=None):
        layer = layer or get_active_layer(get_current_request())
        storage = self.storages.get(app, {}).get(layer, None)
        if storage:
            if layer:
                if storage.exists(path):
                    matched_path = storage.path(path)
                    if matched_path:
                        return matched_path

    def list(self, ignore_patterns, layer=None):
        """
        List all files in all app storages.
        """
        if not layer:
            return

        for storage in self.storages.itervalues():
            layer_storage = storage.get(layer, None)
            if layer_storage and layer_storage.exists(''):
                for path in utils.get_files(layer_storage, ignore_patterns):
                    yield path, layer_storage
