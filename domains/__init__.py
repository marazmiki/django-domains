# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from django.conf import settings
from domains.utils import SiteIDHook


settings.SITE_ID = SiteIDHook()
