# -*- encoding: utf-8 -*-
# ! python2

from __future__ import (absolute_import, division, print_function, unicode_literals)

from unittest import TestCase

from django_make_app.renderers import TemplateRenderer
from django_make_app.structure import prepare_structure, SIMPLE_ROOT, get_next_item_name, generate_model_items, generate_template_items


class DummyTemplateRenderer(object):
    def __init__(self, *args, **kwargs):
        pass

    def render(self, template_name, contenxt):
        return "{}".format(template_name)


class StructureTestCase(TestCase):
    def test_prepare_structure(self):
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

        in_app_schema = {
            "name": "web_app",
            "models": [
                {"name": "Library"},
                {"name": "Book"}
            ]
        }

        self.assertDictEqual(expected_structure, prepare_structure(in_structure, in_app_schema))

    def test_generate_model_items(self):
        model_list = [
            {
                "name": "Book"
            }, {
                "name": "Library"
            }
        ]

        expected = [{"type": "file", "name": "test_book.py", "template_name": "tests/model_test.jinja2.html", "renderer": TemplateRenderer, "_model": {"name": "Book"}},
                    {"type": "file", "name": "test_library.py", "template_name": "tests/model_test.jinja2.html", "renderer": TemplateRenderer, "_model": {"name": "Library"}}]

        self.assertListEqual(expected, [i for i in generate_model_items(model_list)])

    def test_generate_template_items(self):
        model_list = [
            {
                "name": "Book"
            }
        ]

        expected = [
            {
                "type": "file",
                "name": "book_detail.html",
                "template_name": "templates/detail.jinja2.html",
                "renderer": TemplateRenderer,
                "_model": {"name": "Book"}
            },
            {
                "type": "file",
                "name": "book_form.html",
                "template_name": "templates/form.jinja2.html",
                "renderer": TemplateRenderer,
                "_model": {"name": "Book"}
            },
            {
                "type": "file",
                "name": "book_list.html",
                "template_name": "templates/list.jinja2.html",
                "renderer": TemplateRenderer,
                "_model": {"name": "Book"}
            },
            {
                "type": "file",
                "name": "book_delete.html",
                "template_name": "templates/delete.jinja2.html",
                "renderer": TemplateRenderer,
                "_model": {"name": "Book"}
            }
        ]

        self.assertListEqual(expected, [i for i in generate_template_items(model_list)])


class SimpleFolderTestCase(TestCase):
    def test_xx(self):
        self.assertEqual(SIMPLE_ROOT, get_next_item_name(is_folder=True, item_name="foo", app_name="foo", current_root=SIMPLE_ROOT))
        self.assertEqual("foo/", get_next_item_name(is_folder=True, item_name="foo", app_name="bar", current_root=SIMPLE_ROOT))
        self.assertEqual("some/path/foo/", get_next_item_name(is_folder=True, item_name="foo", app_name="bar", current_root="some/path/"))
        self.assertEqual("some/path/", get_next_item_name(is_folder=False, item_name="foo", app_name="bar", current_root="some/path/"))
