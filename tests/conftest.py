#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest

from flask import Flask
from flask_styleguide import key
from flask_styleguide import Styleguide


def create_app(import_name=__name__, static_path=None,
               static_url_path=None, static_folder='static',
               template_folder='templates', instance_path=None,
               instance_relative_config=False, **options):
    """Application factory."""
    app = Flask(import_name, static_path, static_url_path, static_folder,
                template_folder, instance_path, instance_relative_config)

    for name, value in options.items():
        app.config[name.upper()] = value

    return app


@pytest.fixture()
def app(request):
    """Use `pytest.mark` decorator to pass options to your application
    factory::

        @pytest.mark.options(static_folder='assets')
        def test_app(app):
            pass

    Set options to extension, e.g.::

        @pytest.mark.config(foo=42)
        def test_app(app):
            pass

    """
    options = dict(debug=True, testing=True, secret='secret')

    # Update application options from pytest environment
    if 'options' in request.keywords:
        options.update(request.keywords['options'].kwargs)

    app = create_app(**options)

    # Update extension options from pytest environment
    if 'config' in request.keywords:
        for name, value in request.keywords['config'].kwargs.items():
            app.config[key(name)] = value

    Styleguide(app)

    return app


@pytest.fixture()
def client(app):
    """Test client for application."""
    return app.test_client()


@pytest.fixture()
def config(app):
    """Application config."""
    return app.config
