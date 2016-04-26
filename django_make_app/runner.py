# -*- encoding: utf-8 -*-
# ! python2

from __future__ import (absolute_import, division, print_function)

import logging
import os
import shutil

import click

from django_make_app.generators import TemplateFileAppGenerator
from django_make_app.io_utils import read_yaml_file
from django_make_app.schema import normalize_schema
from django_make_app.structure import get_structure

logger = logging.getLogger(__name__)
click.disable_unicode_literals_warning = False


@click.command()
@click.option('--force', is_flag=True)
@click.option('--no-optimize', is_flag=True)
@click.option('-v', '--verbose', count=True)
@click.option('-w', '--quiet', count=True)
def main(force, no_optimize, verbose, quiet):
    logging.basicConfig(level=logging.WARN + 10 * quiet - 10 * verbose)

    this_dir = os.path.dirname(os.path.realpath(__file__))
    templates_dir = os.path.join(this_dir, "templates")

    yaml_raw_data = read_yaml_file(os.path.join(this_dir, "example.yaml"))
    normalized_data = normalize_schema(yaml_raw_data)

    app_target_path = os.path.join(this_dir, normalized_data.get('app_name'))

    if force and os.path.exists(app_target_path):
        logger.info("Deleting {}".format(app_target_path))
        shutil.rmtree(app_target_path)

    structure_of_app = get_structure(normalized_data)

    app_generator = TemplateFileAppGenerator(this_dir, templates_dir, normalized_data, structure_of_app)

    logger.info("Generating app")
    app_generator.generate_app()

    if not no_optimize:
        logger.info("Optimizing source code")
        app_generator.optimize_source_codes()

    click.echo('Done')


if __name__ == '__main__':
    main()
