# -*- encoding: utf-8 -*-
# ! python2

from __future__ import (absolute_import, division, print_function, unicode_literals)

import re

from django_make_app.exceptions import SchemaError
from django_make_app.utils import is_callable

MODEL_NAME_RE = re.compile(ur'^[a-zA-Z_][a-zA-Z0-9_]*$')


class YamlSchemaKeywords(object):
    APP_NAME = "app_name"
    MODELS = "models"


class StructureKeyword(object):
    NAME = "name"
    TYPE = "type"
    FOLDER = "folder"
    FILE = "file"
    RENDERER = "renderer"
    ITEMS = "items"
    TARGET_FILENAME = "_target_filename"
    TEMPLATE_NAME = "template_name"


MAPPINGS = {
    # Relations
    "fk": (lambda field_name: "ForeignKey(\"__app__.{to}\")".format(to=field_name.title())),
    "o2o": (lambda field_name: "ForeignKey(\"{to}\")".format(to=field_name)),
    "m2m": (lambda field_name: "ForeignKey(\"{to}\")".format(to=field_name)),

    # Types
    "text": (lambda *args, **kwargs: "TextField()"),
    "char": (lambda *args, **kwargs: "CharField(max_length=\"{max_length}\")".format(max_length=255)),
    "boolean": (lambda *args, **kwargs: "BooleanField()"),
    "date": (lambda *args, **kwargs: "DateField()"),
    "datetime": (lambda *args, **kwargs: "DateTimeField()"),
    "decimal": (lambda *args, **kwargs: "DecimalField()"),
    "filepath": (lambda *args, **kwargs: "FilePathField()"),
    "float": (lambda *args, **kwargs: "FloatField()"),
    "integer": (lambda *args, **kwargs: "IntegerField()"),
    "ip": (lambda *args, **kwargs: "IPAddressField()"),
    "gip": (lambda *args, **kwargs: "GenericIPAddressField()"),
    "nboolean": (lambda *args, **kwargs: "NullBooleanField()"),
    "time": (lambda *args, **kwargs: "TimeField()"),
    "binary": (lambda *args, **kwargs: "BinaryField()"),
    "auto": (lambda *args, **kwargs: "AutoField()"),
}


def normalize_single_field(field):
    """
    :type field: unicode
    :rtype: dict
    """
    field_name, field_type = field.split(":")

    if not field_type or field_type not in MAPPINGS:
        raise SchemaError("Type {} is invalid".format(field_type))

    field_class = MAPPINGS.get(field_type)

    return {
        "name": field_name,
        "class": field_class(field_name) if is_callable(field_class) else field_class
    }


def normalize_fields(fields):
    """
    :type fields: list of unicode
    :rtype: dict
    """
    for field in fields:
        yield normalize_single_field(field)


def validate_model_name(model_name):
    if not re.search(MODEL_NAME_RE, model_name):
        raise SchemaError("\"{}\" is not a valid name of Django model.".format(model_name))


def normalize_single_model(model):
    """
    In e.g.: {'User': ['name', 'email']}

    :type model: dict
    :rtype: dict
    """
    for model_name, model_fields in model.iteritems():
        validate_model_name(model_name)

        return {
            "name": model_name,
            "fields": [f for f in normalize_fields(model_fields)]
        }


def normalize_single_plain_model(model):
    """
    :type model: unicode
    :rtype: dict
    """
    validate_model_name(model)

    return {
        "name": model,
        "fields": []
    }


def normalize_models(models_list):
    """
    :type models_list: list
    :rtype: list
    """
    for model in models_list:
        if not isinstance(model, dict):
            yield normalize_single_plain_model(model)
        else:
            yield normalize_single_model(model)


def normalize_schema(innn):
    """
    :type innn: dict
    :rtype: dict
    """
    app_name = innn.get(YamlSchemaKeywords.APP_NAME)
    normalized_models = [i for i in normalize_models(innn.get(YamlSchemaKeywords.MODELS))]

    for model in normalized_models:
        for field in model.get('fields'):
            field['class'] = field['class'].replace("__app__", app_name)

    return {
        YamlSchemaKeywords.APP_NAME: app_name,
        YamlSchemaKeywords.MODELS: normalized_models
    }
