# -*- encoding: utf-8 -*-
# ! python2

from __future__ import (absolute_import, division, print_function, unicode_literals)

from unittest import TestCase

import yaml

from django_make_app.exceptions import SchemaError
from django_make_app.schema import normalize_schema, normalize_single_plain_model


class SchemaTestCase(TestCase):
    def test_normalize_single_plain_model(self):
        inv = "Book - library:fk"

        self.assertRaises(SchemaError, normalize_single_plain_model, inv)

    def test_normalization(self):
        self.maxDiff = None

        inn = yaml.load("""
        app_name: web
        models:
          - User:
            - name:char
            - email:text
          - Book:
            - library:fk
          - Library
        """)

        outtt = {
            'app_name': 'web',
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
