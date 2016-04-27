# -*- encoding: utf-8 -*-
# ! python2

from __future__ import (absolute_import, division, print_function, unicode_literals)

import io
import os
from unittest import TestCase

import click
from click.testing import CliRunner

from django_make_app.runner import cli, YAML_FILENAME

click.disable_unicode_literals_warning = True


class RunnerTestCase(TestCase):
    OK_CODE = 0
    CATCHALL_FOR_GENERAL_ERRORS_CODE = 1
    MISUSE_OF_SHELL_BUILTING_CODE = 2

    @staticmethod
    def _get_example_schema():
        templates_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "django_make_app", u"templates", u"example.yaml")

        with io.open(templates_dir, mode='r', encoding='utf-8') as the_file:
            content = the_file.read()

        return content

    def test_write_config(self):
        runner = CliRunner()

        write_only_help = runner.invoke(cli, ['write_config', '--help'])
        self.assertEqual(self.OK_CODE, write_only_help.exit_code)
        self.assertIn(u"write_config [OPTIONS]", write_only_help.output)

        write_real = runner.invoke(cli, ['write_config'])
        self.assertEqual(self.OK_CODE, write_real.exit_code)

        example_schema = self._get_example_schema()
        self.assertEqual(example_schema + "\n", write_real.output)

    def test_generate(self):
        runner = CliRunner()

        with runner.isolated_filesystem():
            with io.open(YAML_FILENAME, mode='w', encoding='utf-8') as the_file:
                the_file.write(self._get_example_schema())

            generate_no_app_arg_given = runner.invoke(cli, ['generate'])
            self.assertEqual(self.MISUSE_OF_SHELL_BUILTING_CODE, generate_no_app_arg_given.exit_code)
            self.assertIn("Missing argument \"app\"", generate_no_app_arg_given.output)

            generate_unknown_app = runner.invoke(cli, ['generate', 'foooo'])
            self.assertEqual(self.MISUSE_OF_SHELL_BUILTING_CODE, generate_unknown_app.exit_code)
            self.assertIn("App not found", generate_unknown_app.output)

            generate_ok = runner.invoke(cli, ['generate', 'library'])
            self.assertEqual(self.OK_CODE, generate_ok.exit_code)

            generate_already_exists = runner.invoke(cli, ['generate', 'library', '--no-optimize'])
            self.assertEqual(self.CATCHALL_FOR_GENERAL_ERRORS_CODE, generate_already_exists.exit_code)
            self.assertIn("already exists", generate_already_exists.output)

            generate_already_exists_force = runner.invoke(cli, ['generate', 'library', '--no-optimize', '--force'])
            self.assertEqual(self.OK_CODE, generate_already_exists_force.exit_code)
