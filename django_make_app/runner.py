# -*- encoding: utf-8 -*-
# ! python2

from __future__ import (absolute_import, division, print_function)

import io
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


@click.group()
def cli():
    pass


@cli.command()
def write_config():
    templates_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "templates", "example.yaml")

    with io.open(templates_dir, mode='r', encoding='utf-8') as the_file:
        click.echo(the_file.read())


@cli.command()
@click.argument('app')
@click.option('--force', is_flag=True, help="Overwrite app directory, do not validate app argument.")
@click.option('--no-optimize', is_flag=True, help="Do not optimize generated source code using yapf and isort.")
@click.option('-v', '--verbose', count=True)
@click.option('-w', '--quiet', count=True)
def generate(app, force, no_optimize, verbose, quiet):
    """
    app: this will be resolved to os.getcwd()/{app}.yml
    """
    logging.basicConfig(level=logging.WARN + 10 * quiet - 10 * verbose)

    cwd = os.getcwd()
    this_dir = os.path.dirname(os.path.realpath(__file__))
    templates_dir = os.path.join(this_dir, "templates")

    yaml_raw_data = read_yaml_file(os.path.join(cwd, "{}.yaml".format(app)))
    normalized_data = normalize_schema(yaml_raw_data)
    app_name = normalized_data.get('app_name')

    if not force and app != app_name:
        click.confirm('app argument (\"{0}\") != app defined in {0}.yaml (\"{1}\"). Do you want to continue?'.format(app, app_name), abort=True)

    app_target_path = os.path.join(cwd, app_name)

    if os.path.exists(app_target_path):
        if force:
            logger.info("Deleting {}".format(app_target_path))
            shutil.rmtree(app_target_path)
        else:
            raise click.ClickException('Path: %s already exists.' % click.format_filename(app_target_path))

    structure_of_app = get_structure(normalized_data)
    app_generator = TemplateFileAppGenerator(cwd, templates_dir, normalized_data, structure_of_app)

    logger.info("Generating app")
    app_generator.generate_app()

    if not no_optimize:
        logger.info("Optimizing source code")
        app_generator.optimize_source_codes()

    click.echo('Done')


if __name__ == '__main__':
    cli()
