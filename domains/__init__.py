# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from domains.utils import get_hooks, setup_hook

for hook in get_hooks():
    setup_hook(hook)
