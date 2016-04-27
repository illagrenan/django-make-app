# -*- encoding: utf-8 -*-
# ! python2

from __future__ import (absolute_import, division, print_function, unicode_literals)

from django_make_app.renderers import TemplateRenderer
from django_make_app.schema import YamlSchemaKeywords, StructureKeyword
from django_make_app.utils import is_callable


def generate_template_items(model_list):
    operations = ["detail", "form", "list", "delete"]

    for model in model_list:
        for operation in operations:
            yield {
                "type": "file",
                "name": "{}_{}.html".format(model.get('name').lower(), operation),
                "template_name": "templates/{}.jinja2.html".format(operation),
                "renderer": TemplateRenderer,
                "_model": model
            }


def generate_model_items(model_list):
    for model in model_list:
        yield {
            "type": "file",
            "name": "test_{}.py".format(model.get('name').lower()),
            "template_name": "tests/model_test.jinja2.html",
            "renderer": TemplateRenderer,
            "_model": model
        }


APP_STRUCTURE = {
    "type": "folder",
    "name": "__app__",
    "is_package": True,
    "items": [
        {
            "type": "file",
            "name": "__init__.py",
            "renderer": TemplateRenderer
        },
        {
            "type": "file",
            "name": "admin.py",
            "renderer": TemplateRenderer
        },
        {
            "type": "file",
            "name": "api.py",
            "renderer": TemplateRenderer
        },
        {
            "type": "file",
            "name": "apps.py",
            "renderer": TemplateRenderer
        },
        {
            "type": "file",
            "name": "checks.py",
            "renderer": TemplateRenderer
        },
        {
            "type": "file",
            "name": "forms.py",
            "renderer": TemplateRenderer
        },
        {
            "type": "file",
            "name": "models.py",
            "renderer": TemplateRenderer
        },
        {
            "type": "file",
            "name": "receivers.py",
            "renderer": TemplateRenderer
        },
        {
            "type": "file",
            "name": "serializers.py",
            "renderer": TemplateRenderer
        },
        {
            "type": "file",
            "name": "signals.py",
            "renderer": TemplateRenderer
        },
        {
            "type": "file",
            "name": "urls.py",
            "renderer": TemplateRenderer
        },
        {
            "type": "file",
            "name": "views.py",
            "renderer": TemplateRenderer
        },
        {
            "type": "folder",
            "name": "migrations",
            "is_package": True,
            "items": [
                {
                    "type": "file",
                    "name": "__init__.py",
                    "renderer": TemplateRenderer
                },
            ]
        },
        {
            "type": "folder",
            "name": "templates",
            "is_package": False,
            "items": [
                {
                    "type": "folder",
                    "name": "__app__",
                    "is_package": False,
                    "items": [
                        generate_template_items
                    ]
                }
            ]
        },
        {
            "type": "folder",
            "name": "templatetags",
            "is_package": True,
            "items": [
                {
                    "type": "file",
                    "name": "__init__.py",
                    "renderer": TemplateRenderer
                },
                {
                    "type": "file",
                    "name": "__app___tags.py",
                    "template_name": "templatetags/template_tags.jinja2.html",
                    "renderer": TemplateRenderer
                }
            ]
        },
        {
            "type": "folder",
            "name": "tests",
            "is_package": True,
            "items": [
                {
                    "type": "file",
                    "name": "__init__.py",
                    "renderer": TemplateRenderer
                },
                {
                    "type": "file",
                    "name": "factories.py",
                    "renderer": TemplateRenderer
                },
                generate_model_items
            ]
        },
        {
            "type": "folder",
            "name": "management",
            "is_package": True,
            "items": [
                {
                    "type": "file",
                    "name": "__init__.py",
                    "renderer": TemplateRenderer
                },
                {
                    "type": "folder",
                    "name": "commands",
                    "is_package": True,
                    "items": [
                        {
                            "type": "file",
                            "name": "__init__.py",
                            "renderer": TemplateRenderer
                        },
                        {
                            "type": "file",
                            "name": "__app___command.py",
                            "template_name": "management/commands/management_commands.jinja2.html",
                            "renderer": TemplateRenderer
                        }
                    ]
                }
            ]
        },
    ]

}

SIMPLE_ROOT = ""


def get_next_item_name(is_folder, item_name, app_name, current_root):
    """
    :type is_folder: bool
    :type item_name: unicode
    :type app_name: unicode
    :type current_root: unicode
    :rtype: unicode
    """
    if not is_folder:
        return current_root

    if item_name == app_name and current_root == SIMPLE_ROOT:
        # app directory only in root is root
        return SIMPLE_ROOT

    return "{}{}/".format(current_root, item_name)


def get_structure(data):
    return prepare_structure(APP_STRUCTURE, data)


def prepare_structure(structure_item, app_data, simple_folder_path=SIMPLE_ROOT):
    models_list = app_data.get(YamlSchemaKeywords.MODELS)
    app_name = app_data.get(YamlSchemaKeywords.APP_NAME)
    item_type = structure_item.get(StructureKeyword.TYPE)
    is_folder = item_type == StructureKeyword.FOLDER
    is_file = item_type == StructureKeyword.FILE

    nodes = []

    for node_obj in structure_item.get(StructureKeyword.ITEMS, []):
        if is_callable(node_obj):
            nodes = nodes + [generated_node for generated_node in node_obj(models_list)]
        else:
            nodes.append(node_obj)

    new_item_name = structure_item.get(StructureKeyword.NAME).replace('__app__', app_name)
    next_item_simple_path = get_next_item_name(is_folder, new_item_name, app_name, simple_folder_path)

    return_dict = dict(structure_item)
    return_dict.update({
        StructureKeyword.NAME: new_item_name
    })

    if StructureKeyword.TEMPLATE_NAME not in return_dict and is_file:
        return_dict.update({
            StructureKeyword.TEMPLATE_NAME: "{}{}.jinja2.html".format(next_item_simple_path, new_item_name)
        })

    if nodes:
        # Prevent empty [] for better readability
        return_dict.update({
            StructureKeyword.ITEMS: [prepare_structure(node, app_data, next_item_simple_path) for node in nodes]
        })

    return return_dict
