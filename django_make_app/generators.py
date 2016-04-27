# -*- encoding: utf-8 -*-
# ! python2

from __future__ import (absolute_import, division, print_function, unicode_literals)

import io
import logging
import os

import glob2

from django_make_app.io_utils import optimize_code
from django_make_app.schema import YamlSchemaKeywords, StructureKeyword

logger = logging.getLogger(__name__)


class TemplateFileAppGenerator(object):
    def __init__(self, base_directory, templates_directory, app_data, app_structure):
        self._base_directory = base_directory
        self._templates_directory = templates_directory
        self._app_data = app_data
        self._app_structure = app_structure

    def optimize_source_codes(self):
        path_to_app = os.path.normpath(os.path.join(self._base_directory, self._app_data.get(YamlSchemaKeywords.APP_NAME), "**/*.py"))

        for filename in glob2.glob(path_to_app):
            logger.debug("Optimizing {}".format(filename))
            optimize_code(filename)

    def generate_app(self):
        self._create_app_structure(self._base_directory, self._app_structure)

    def _render(self, rendered_class, item):
        return rendered_class(templates_directory=self._templates_directory, template_name=item.get(StructureKeyword.TEMPLATE_NAME), item=item).render(context=self._app_data)

    def _create_app_structure(self, base_directory, structure):
        item_type = structure.get(StructureKeyword.TYPE)
        item_name = structure.get(StructureKeyword.NAME)
        is_folder = item_type == StructureKeyword.FOLDER
        is_file = item_type == StructureKeyword.FILE

        target_path = os.path.join(base_directory, item_name)

        if is_folder:
            new_base_dir = target_path
            self._make_directory(target_path)
        elif is_file:
            new_base_dir = os.path.dirname(target_path)
            self._make_file(structure, target_path)
        else:
            raise ValueError("Unknown item type {}".format(item_type))

        for node_obj in structure.get(StructureKeyword.ITEMS, []):
            self._create_app_structure(new_base_dir, node_obj)

    def _make_file(self, structure, target_path):
        renderer = structure.get(StructureKeyword.RENDERER)

        with io.open(target_path, encoding='utf-8', mode="w+") as the_file:
            the_file.write(self._render(renderer, structure))

    def _make_directory(self, target_path):
        os.mkdir(target_path)
