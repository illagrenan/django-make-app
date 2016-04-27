# -*- encoding: utf-8 -*-
# ! python2

from __future__ import (absolute_import, division, print_function, unicode_literals)

import os
import shutil
import tempfile
from unittest import TestCase

from django_make_app.generators import TemplateFileAppGenerator
from django_make_app.renderers import TemplateRenderer


class GeneratorsTestCase(TestCase):
    def setUp(self):
        super(GeneratorsTestCase, self).setUp()
        self.dirpath = tempfile.mkdtemp()

    def tearDown(self):
        super(GeneratorsTestCase, self).tearDown()
        shutil.rmtree(self.dirpath)

    def test_generate(self):
        this_dir = os.path.dirname(os.path.realpath(__file__))
        templates_dir = os.path.join(this_dir, "..", "django_make_app", "templates")

        expected_structure = {
            "type": "folder",
            "name": "web_app",
            "items": [
                {
                    "type": "file",
                    "name": "__init__.py",
                    "template_name": "__init__.py.jinja2.html",
                    "renderer": TemplateRenderer
                },
                {
                    "type": "file",
                    "name": "admin.py",
                    "template_name": "admin.py.jinja2.html",
                    "renderer": TemplateRenderer
                },
                {
                    "type": "file",
                    "name": "api.py",
                    "template_name": "api.py.jinja2.html",
                    "renderer": TemplateRenderer
                },
                {
                    "type": "folder",
                    "name": "tests",
                    "items": [
                        {
                            "type": "file",
                            "name": "test_article.py",
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
                            "renderer": TemplateRenderer
                        }
                    ]
                }
            ]
        }

        in_app_schema = {
            "name": "web_app",
            "models": [
                {"name": "Article"},
                {"name": "Book"}
            ]
        }

        app_generator = TemplateFileAppGenerator(self.dirpath, templates_dir, in_app_schema, expected_structure)
        app_generator.generate_app()

        expected_generated_items = [
            os.path.join(self.dirpath, "web_app"),
            os.path.join(self.dirpath, "web_app", "admin.py"),
            os.path.join(self.dirpath, "web_app", "api.py"),
            os.path.join(self.dirpath, "web_app", "tests"),
            os.path.join(self.dirpath, "web_app", "tests", "test_book.py"),
            os.path.join(self.dirpath, "web_app", "tests", "test_article.py"),
            os.path.join(self.dirpath, "web_app", "tests", "__init__.py"),
            os.path.join(self.dirpath, "web_app", "__init__.py"),
        ]

        for path_to_check in expected_generated_items:
            self.assertTrue(os.path.exists(path_to_check), msg="{0} does not exist".format(path_to_check))

    def test_generate_with_invalid_structure(self):
        this_dir = os.path.dirname(os.path.realpath(__file__))
        templates_dir = os.path.join(this_dir, "..", "django_make_app", "templates")

        expected_structure = {
            "type": "folder",
            "name": "web_app",
            "items": [
                {
                    "type": "unicorn",
                    "name": "__init__.py",
                    "template_name": "__init__.py.jinja2.html",
                    "renderer": TemplateRenderer
                }
            ]
        }

        in_app_schema = {
            "name": "web_app",
            "models": [
                {"name": "Article"},
                {"name": "Book"}
            ]
        }

        app_generator = TemplateFileAppGenerator(self.dirpath, templates_dir, in_app_schema, expected_structure)
        self.assertRaises(ValueError, app_generator.generate_app)
