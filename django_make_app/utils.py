# -*- encoding: utf-8 -*-
# ! python2

from __future__ import (absolute_import, division, print_function, unicode_literals)


def is_callable(obj):
    return hasattr(obj, '__call__')
