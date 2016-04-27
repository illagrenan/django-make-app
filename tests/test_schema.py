# -*- encoding: utf-8 -*-
# ! python2

from __future__ import (absolute_import, division, print_function, unicode_literals)

from unittest import TestCase

import yaml

from django_make_app.exceptions import SchemaError
from django_make_app.schema import normalize_schema, validate_model_name, normalize_single_field


class SchemaTestCase(TestCase):
    def test_validate_model_name(self):
        wrong_model_name = "Book - library:fk"

        self.assertRaises(SchemaError, validate_model_name, wrong_model_name)

        validate_model_name("OkName")
        validate_model_name("Book")
        validate_model_name("Library")

    def test_normalize_single_field(self):
        expected_value = {"name": "my_name", "class": "IntegerField()"}
        self.assertDictEqual(expected_value, normalize_single_field("my_name:integer"))

    def test_normalization(self):
        self.maxDiff = None

        inn = yaml.load("""
        name: web
        models:
          - User:
            - name:char
            - email:text
          - Book:
            - library:fk
          - Library
        """)

        outtt = {
            'name': 'web',
            'models': [
                {
                    'name': 'User',
                    "fields": [
                        {
                            "name": "name",
                            "class": "CharField(max_length=\"255\")"
                        },
                        {
                            "name": "email",
                            "class": "TextField()"
                        }
                    ]
                },
                {
                    'name': 'Book',
                    "fields": [
                        {
                            'name': 'library',
                            'class': 'ForeignKey("web.Library")',
                        }
                    ]
                },
                {
                    'name': 'Library',
                    "fields": []
                },

            ]
        }

        self.assertDictEqual(outtt, normalize_schema(inn))
