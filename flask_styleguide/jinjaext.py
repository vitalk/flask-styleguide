#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    flask_styleguide.jinjaext
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    Jinja extension to render KSS Style Guide.

    :copyright: (c) 2014 by Vital Kudzelka <vital.kudzelka@gmail.com>
    :license: MIT
"""
import textwrap
from jinja2 import nodes
from jinja2 import Template
from jinja2.ext import Extension
from pykss.exceptions import SectionDoesNotExist

from .compat import text_type


class StyleguideExtension(Extension):
    """Add `styleguide` tag to jinja environment to automatically generate
    a living styleguide from KSS documentation syntax.

    .. sourcecode:: html+jinja

        {% styleguide 1.1 %}
            <button class="button$modifier_class">Button</button>
        {% endstyleguide %}

    """
    tags = set(['styleguide'])

    def __init__(self, environment):
        super(StyleguideExtension, self).__init__(environment)

        # Add the defaults to the environment
        environment.extend(
            styleguide_kss_parser=None,
            styleguide_template_name=None,
        )

    def parse(self, parser):
        lineno = parser.stream.next().lineno

        # Parse a single expression that is used as guide reference.
        args = [parser.parse_expression()]

        # Parse the body until end of the block
        body = parser.parse_statements(['name:endstyleguide'], drop_needle=True)

        call = self.call_method('_render', args)
        call_block = nodes.CallBlock(call, (), (), body)
        call_block.set_lineno(lineno)
        return call_block

    def _render(self, reference, caller):
        """Render styleguide section on which identifier reference to.

        :param ref: The section reference in styleguide to render.
        """
        example_html = textwrap.dedent(caller())
        reference = text_type(reference)
        kss_parser = self.environment.styleguide_kss_parser
        template_name = self.environment.styleguide_template_name

        if template_name is None:
            return ''
        template = self.environment.get_template(template_name)

        sections = sorted([sec for ref, sec in
            kss_parser.sections.items() if ref.startswith(reference)],
            key=lambda x: x.section)

        for section in sections:
            section.add_example(example_html)

        out = [template.render(section=section) for section in sections]
        return ''.join(out)
