#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import pytest
import shutil
import tempfile
import textwrap

from pykss import Parser
from jinja2 import Template
from jinja2 import Environment
from jinja2 import FileSystemLoader

from flask_styleguide.jinjaext import StyleguideExtension


class TempdirHelper(object):
    """Base class which provides a temporary directory to each test suite."""

    default_files = {}

    def setup(self):
        """Create temporary directory and create required files."""
        self._tempdir = tempfile.mkdtemp()
        self.create_files(self.default_files)

    def teardown(self):
        """Remove temporary directory tree."""
        shutil.rmtree(self.tempdir)

    @property
    def tempdir(self):
        """Read-only property to prevent tempdir modifications."""
        return self._tempdir

    def create_files(self, files):
        """Create files for test suite. Use list to create empty files."""
        if not hasattr(files, 'items'):
            files = dict((filename, '') for filename in files)
        for filename, data in files.items():
            path = self.path(filename)
            directory = os.path.dirname(path)
            if not os.path.exists(directory):
                os.makedirs(directory)
            with open(path, 'w') as outfile:
                outfile.write(data)

    def path(self, filename):
        """Returns full path for the given filename in tempdir."""
        return os.path.join(self.tempdir, filename)


class TestJinjaExtension(TempdirHelper):

    default_files = {
        'static/buttons.css': """
            /*
            A classic form button.

            :hover - Highlights on hover.
            :disabled - Mute inactive buttons.

            Styleguide 1.1
            */
            .button {}
        """,
        'static/minibuttons.css': """
            /*
            A mini button.

            :hover - Highlights on hover.
            :disabled - Mute inactive buttons.

            Styleguide 1.2
            */
            .minibutton {}
        """,
        'templates/custom.html': "{{ section.section }}{{ section.example }}\n\n",
    }

    def setup(self):
        super(TestJinjaExtension, self).setup()

        self.jinja_env = Environment()
        self.jinja_env.add_extension(StyleguideExtension)
        self.jinja_env.loader = FileSystemLoader('%s/templates' % self.tempdir)
        self.jinja_env.styleguide_kss_parser = Parser('%s/static' % self.tempdir)
        self.jinja_env.styleguide_template_name = 'custom.html'

    def render_template(self, ref, example=''):
        template_string = (
            "{%% styleguide %(ref)s %%}"
            "%(example)s"
            "{%% endstyleguide %%}"
        ) % dict(ref=ref, example=example)

        template = self.jinja_env.from_string(template_string)
        return template.render()

    def test_render_section(self):
        assert self.render_template('1.1') == '1.1\n'

    def test_render_subsections_as_well(self):
        assert self.render_template('1') == '1.1\n1.2\n'

    def test_render_when_section_does_not_exist(self):
        assert self.render_template('0') == ''

    def test_kss_parser_caches_output(self):
        assert self.render_template('1') == '1.1\n1.2\n'

        self.create_files(('static/buttons.css', 'static/minibuttons.css'))
        assert self.render_template('1') == '1.1\n1.2\n'

    def test_dedent_example(self):
        example_html = """
        <button>
            <i></i>
        </button>
        """
        expected_html = textwrap.dedent(example_html)
        assert self.render_template('1.1', example_html) == '1.1%s\n' % expected_html
