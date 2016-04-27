# -*- encoding: utf-8 -*-
# ! python2

from __future__ import (absolute_import, division, print_function, unicode_literals)

from unittest import TestCase

from django_make_app.utils import is_callable


def dummy_callable():
    for _ in range(2):
        yield {
            "name": "X",
            "nodes": []
        }


def unpack_callables_in_dict(item):
    nodes = []

    for node in item.get("nodes", []):
        if is_callable(node):
            nodes = nodes + [generated_node for generated_node in node()]
        else:
            nodes.append(node)

    return {
        "name": item.get('name'),
        "nodes": [unpack_callables_in_dict(node) for node in nodes]
    }


class DictRecursiveUnpackTestCase(TestCase):
    def test_recursion(self):
        self.maxDiff = None

        in_structure = {
            "name": "A",
            "nodes": [
                {
                    "name": "AB"
                },
                dummy_callable

            ]
        }

        expected_structure = {
            "name": "A",
            "nodes": [
                {
                    "name": "AB",
                    "nodes": []
                },
                {
                    "name": "X",
                    "nodes": []
                },
                {
                    "name": "X",
                    "nodes": []
                }
            ]
        }

        self.assertDictEqual(expected_structure, unpack_callables_in_dict(in_structure))


class DictRecursiveUnpackComplexTestCase(TestCase):
    def test_recursion(self):
        self.maxDiff = None

        in_structure = {
            "name": "A",
            "nodes": [
                {
                    "name": "AA",
                    "nodes": [
                        dummy_callable,
                        dummy_callable,
                        {
                            "name": "AAA",
                            "nodes": [
                                dummy_callable,
                                dummy_callable,
                            ]
                        },
                        dummy_callable
                    ]
                },
                {
                    "name": "AB",
                    "nodes": [
                        dummy_callable
                    ]
                }
            ]
        }

        expected_structure = {
            "name": "A",
            "nodes": [
                {
                    "name": "AA",
                    "nodes": [
                        {
                            "name": "X",
                            "nodes": []
                        },
                        {
                            "name": "X",
                            "nodes": []
                        },
                        {
                            "name": "X",
                            "nodes": []
                        },
                        {
                            "name": "X",
                            "nodes": []
                        },
                        {
                            "name": "AAA",
                            "nodes": [
                                {
                                    "name": "X",
                                    "nodes": []
                                },
                                {
                                    "name": "X",
                                    "nodes": []
                                },
                                {
                                    "name": "X",
                                    "nodes": []
                                },
                                {
                                    "name": "X",
                                    "nodes": []
                                },
                            ]
                        },
                        {
                            "name": "X",
                            "nodes": []
                        },
                        {
                            "name": "X",
                            "nodes": []
                        }
                    ]
                },
                {
                    "name": "AB",
                    "nodes": [
                        {
                            "name": "X",
                            "nodes": []
                        },
                        {
                            "name": "X",
                            "nodes": []
                        }
                    ]
                }
            ]
        }

        self.assertDictEqual(expected_structure, unpack_callables_in_dict(in_structure))
