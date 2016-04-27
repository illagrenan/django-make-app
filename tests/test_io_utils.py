# -*- encoding: utf-8 -*-
# ! python2

from __future__ import (absolute_import, division, print_function, unicode_literals)

import io
import os
import tempfile
from unittest import TestCase

from django_make_app.io_utils import read_yaml_file, optimize_code


class IOUtilsTestCase(TestCase):
    def test_read_yaml_file(self):
        try:
            with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp:
                temp.write("language: python")

            parsed_yaml = read_yaml_file(temp.name)
        except Exception as e:
            self.fail(e.message)
        finally:
            os.remove(temp.name)

        self.assertDictEqual({'language': 'python'}, parsed_yaml)

    def test_optimize_code(self):
        try:
            with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp:
                temp.write("""\n\n\n\ndef hello():\n\treturn'World'""")

            optimize_code(temp.name)

            with io.open(temp.name, mode="r", encoding="utf-8") as temp_optimized:
                optimized_code = temp_optimized.read()
        except Exception as e:
            self.fail(e)
        finally:
            os.remove(temp.name)

        self.assertEqual("""def hello():\n    return 'World'\n""", optimized_code)
