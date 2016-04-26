# -*- encoding: utf-8 -*-
# ! python2

from __future__ import (absolute_import, division, print_function, unicode_literals)


class InvalidConfiguration(Exception):
    pass


class MissingConfiguration(Exception):
    pass


class FabricException(Exception):
    pass


class SchemaError(Exception):
    pass
