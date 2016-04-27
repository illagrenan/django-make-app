# -*- encoding: utf-8 -*-
# ! python2

from __future__ import (absolute_import, division, print_function, unicode_literals)

from jinja2 import FileSystemLoader, Environment


class TemplateRenderer(object):
    def __init__(self, templates_directory, template_name, item):
        """
        :type templates_directory: os.path
        :type template_name: unicode
        :type item: dict
        """
        self._templates_directory = templates_directory
        self.template_name = template_name
        self.item = item

    def _render_from_template(self, template_name, **kwargs):
        loader = FileSystemLoader(self._templates_directory)
        env = Environment(loader=loader)
        template = env.get_template(template_name)

        render = template.render(**kwargs)

        render = render.replace("[[", "{{")
        render = render.replace("]]", "}}")

        render = render.replace("[%", "{%")
        render = render.replace("%]", "%}")

        return render

    def render(self, context):
        """

        :type context: dict
        """
        if "_model" in self.item:
            context.update({
                "current_model": self.item.get('_model')
            })

        return self._render_from_template(self.template_name, **context)
