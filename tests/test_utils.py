# -*- encoding: utf-8 -*-
# ! python2

from __future__ import (absolute_import, division, print_function, unicode_literals)

import io
import os
from unittest import TestCase

from django_make_app.utils import is_callable


class UtilsTestCase(TestCase):
    def test_is_callable(self):
        self.assertTrue(is_callable(io.open))
        self.assertTrue(is_callable(os.path.join))

        self.assertFalse(is_callable(""))
        self.assertFalse(is_callable(42))
        self.assertFalse(is_callable(None))
        self.assertFalse(is_callable(False))
