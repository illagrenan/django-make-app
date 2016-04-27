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
from django_make_app.schema import normalize_schema, YamlSchemaKeywords
from django_make_app.structure import get_structure

logger = logging.getLogger(__name__)
click.disable_unicode_literals_warning = False

YAML_FILENAME = u"app_schema.yaml"


@click.group()
def cli():
    pass


@cli.command()
def write_config():
    templates_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), u"templates", u"example.yaml")

    with io.open(templates_dir, mode=u'r', encoding=u'utf-8') as the_file:
        click.echo(the_file.read())


@cli.command()
@click.argument(u'app')
@click.option(u'--force', is_flag=True, help=u"Overwrite app directory, do not validate app argument.")
@click.option(u'--no-optimize', is_flag=True, help=u"Do not optimize generated source code using yapf and isort, "
                                                   u"generation will be faster. Also, use this option if "
                                                   u"you're using Python 3.3 (yapf is not compatible with this version).")
@click.option(u'-v', u'--verbose', count=True)
@click.option(u'-w', u'--quiet', count=True)
def generate(app, force, no_optimize, verbose, quiet):
    """
    app: this will be resolved to os.getcwd()/{app}.yml
    """
    logging.basicConfig(level=logging.WARN + 10 * quiet - 10 * verbose)

    cwd = os.getcwd()
    this_dir = os.path.dirname(os.path.realpath(__file__))
    templates_dir = os.path.join(this_dir, u"templates")

    yaml_raw_data = read_yaml_file(os.path.join(cwd, YAML_FILENAME))

    for one_raw_app in yaml_raw_data.get(YamlSchemaKeywords.APPS):
        if one_raw_app.get(YamlSchemaKeywords.APP_NAME) == app:
            target_app = one_raw_app
            break
    else:
        raise click.BadArgumentUsage(u"App not found")

    normalized_data = normalize_schema(target_app)
    app_target_path = os.path.join(cwd, app)

    if os.path.exists(app_target_path):
        if force:
            logger.info(u"Deleting {}".format(app_target_path))
            shutil.rmtree(app_target_path)
        else:
            raise click.ClickException(u'Path: %s already exists.' % click.format_filename(app_target_path))

    structure_of_app = get_structure(normalized_data)
    app_generator = TemplateFileAppGenerator(cwd, templates_dir, normalized_data, structure_of_app)

    logger.info(u"Generating app")
    app_generator.generate_app()

    if not no_optimize:
        logger.info(u"Optimizing source code")
        app_generator.optimize_source_codes()

    click.echo(u'Done')


if __name__ == u'__main__':
    cli()
