# -*- encoding: utf-8 -*-
# ! python2

from __future__ import (absolute_import, division, print_function, unicode_literals)

import os
import tempfile
from unittest import TestCase

from django_make_app.renderers import TemplateRenderer


class RenderersTestCase(TestCase):
    def test_template_renderer(self):
        try:
            with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp:
                temp.write("{{ hello }}")

            templates_directory = os.path.dirname(temp.name)
            template_name = os.path.basename(temp.name)
            renderer = TemplateRenderer(templates_directory=templates_directory, template_name=template_name, item={})

            context = renderer.render(context={
                "hello": "World"
            })
        except Exception as e:
            self.fail(e.message)
        finally:
            os.remove(temp.name)

        self.assertEqual("World", context)
