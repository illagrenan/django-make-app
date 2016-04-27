# -*- encoding: utf-8 -*-
# ! python2

from __future__ import (absolute_import, division, print_function, unicode_literals)

from unittest import TestCase

from django_make_app.renderers import TemplateRenderer
from django_make_app.structure import prepare_structure, SIMPLE_ROOT, get_next_item_name, generate_model_items


class DummyTemplateRenderer(object):
    def __init__(self, *args, **kwargs):
        pass

    def render(self, template_name, contenxt):
        return "{}".format(template_name)


class StructureTestCase(TestCase):
    def test_xx(self):
        self.maxDiff = None

        in_structure = {
            "type": "folder",
            "name": "__app__",
            "items": [
                {
                    "type": "file",
                    "name": "__init__.py",
                    "renderer": DummyTemplateRenderer
                },
                {
                    "type": "file",
                    "name": "admin.py",
                    "renderer": DummyTemplateRenderer
                },
                {
                    "type": "file",
                    "name": "api.py",
                    "renderer": DummyTemplateRenderer
                },
                {
                    "type": "folder",
                    "name": "tests",
                    "items": [
                        generate_model_items,
                        {
                            "type": "file",
                            "name": "__init__.py",
                            "renderer": DummyTemplateRenderer
                        }
                    ]
                }

            ]
        }

        expected_structure = {
            "type": "folder",
            "name": "web_app",
            "items": [
                {
                    "type": "file",
                    "name": "__init__.py",
                    "template_name": "__init__.py.jinja2.html",
                    "renderer": DummyTemplateRenderer
                },
                {
                    "type": "file",
                    "name": "admin.py",
                    "template_name": "admin.py.jinja2.html",
                    "renderer": DummyTemplateRenderer
                },
                {
                    "type": "file",
                    "name": "api.py",
                    "template_name": "api.py.jinja2.html",
                    "renderer": DummyTemplateRenderer
                },
                {
                    "type": "folder",
                    "name": "tests",
                    "items": [
                        {
                            "type": "file",
                            "name": "test_library.py",
                            "template_name": "tests/model_test.jinja2.html",
                            "_model": {"name": "Library"},
                            "renderer": TemplateRenderer
                        },
                        {
                            "type": "file",
                            "name": "test_book.py",
                            "template_name": "tests/model_test.jinja2.html",
                            "_model": {"name": "Book"},
                            "renderer": TemplateRenderer
                        },
                        {
                            "type": "file",
                            "name": "__init__.py",
                            "template_name": "tests/__init__.py.jinja2.html",
                            "renderer": DummyTemplateRenderer
                        }
                    ]
                }
            ]
        }

        in_data = {
            "app_name": "web_app",
            "models": [
                {"name": "Library"},
                {"name": "Book"}
            ]
        }

        self.assertDictEqual(expected_structure, prepare_structure(in_structure, in_data))


class SimpleFolderTestCase(TestCase):
    def test_xx(self):
        self.assertEqual(SIMPLE_ROOT, get_next_item_name(is_folder=True, item_name="foo", app_name="foo", current_root=SIMPLE_ROOT))
        self.assertEqual("foo/", get_next_item_name(is_folder=True, item_name="foo", app_name="bar", current_root=SIMPLE_ROOT))
        self.assertEqual("some/path/foo/", get_next_item_name(is_folder=True, item_name="foo", app_name="bar", current_root="some/path/"))
        self.assertEqual("some/path/", get_next_item_name(is_folder=False, item_name="foo", app_name="bar", current_root="some/path/"))
