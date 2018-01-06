# -*- encoding: utf-8 -*-
# ! python2

from __future__ import (absolute_import, division, print_function, unicode_literals)

import io

import yaml
from isort import SortImports
from yapf.yapflib.yapf_api import FormatFile


def read_yaml_file(filename):
    with io.open(filename, mode='r', encoding='utf-8') as the_file:
        return yaml.safe_load(the_file)


def optimize_code(filename):
    SortImports(filename)
    FormatFile(filename, in_place=True, style_config='{based_on_style: pep8, column_limit: 255}')
