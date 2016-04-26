# -*- encoding: utf-8 -*-
# ! python2

from __future__ import (absolute_import, division, print_function, unicode_literals)

from jinja2 import FileSystemLoader, Environment


class TemplateRenderer(object):
    def __init__(self, templates_directory, template_name):
        self._templates_directory = templates_directory
        self.template_name = template_name

    def _render_from_template(self, template_name, **kwargs):
        loader = FileSystemLoader(self._templates_directory)
        env = Environment(loader=loader)
        template = env.get_template(template_name)

        return template.render(**kwargs)

    def render(self, context):
        return self._render_from_template(self.template_name, **context)
