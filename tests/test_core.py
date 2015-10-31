#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest

from flask import Flask
from flask import Blueprint
from flask_styleguide import key
from flask_styleguide import get_static_paths


class TestExtension(object):

    def test_extension_init(self, app):
        assert app.jinja_env.styleguide_kss_parser is not None
        assert app.jinja_env.styleguide_template_name == 'styleguide/section.html'

    @pytest.mark.options(template_name='custom.html')
    def test_configure_extension(self, app, config):
        assert app.jinja_env.styleguide_template_name == 'custom.html'

    def test_get_static_paths_if_app_has_static_folder(self, app):
        assert get_static_paths(app) == [app.static_folder]

    @pytest.mark.options(static_folder=None)
    def test_get_static_paths_if_app_has_no_static_folder(self, app):
        assert get_static_paths(app) == []

    def test_get_static_paths_if_blueprint_has_static_folder(self, app):
        bp = Blueprint('bp', __name__, static_folder='assets')
        app.register_blueprint(bp)
        assert get_static_paths(app) == [bp.static_folder, app.static_folder]

    def test_get_static_paths_if_blueprint_has_no_static_folder(self, app):
        bp = Blueprint('bp', __name__)
        app.register_blueprint(bp)
        assert get_static_paths(app) == [app.static_folder]

    def test_get_static_paths_if_paths_has_only_unique_entries(self, app):
        bp = Blueprint('bp', __name__, static_folder='static')
        app.register_blueprint(bp)
        assert get_static_paths(app) == [app.static_folder]
