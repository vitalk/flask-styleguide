#!/usr/bin/env python
# -*- coding: utf-8 -*-
import inspect
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
    factory or configure extension::

        @pytest.mark.options(static_folder='assets')
        def test_app(app):
            pass

    """
    options = dict(debug=True, testing=True, secret='secret')
    extra_options = {}

    # Update application options from pytest environment if they names
    # match with factory spec and use them to configure extension otherwise.
    func_spec = inspect.getargspec(create_app)
    if 'options' in request.keywords:
        for name, value in request.keywords['options'].kwargs.items():
            if name in func_spec.args:
                options[name] = value
            else:
                extra_options[key(name)] = value

    app = create_app(**options)
    app.config.update(extra_options)

    Styleguide(app)

    return app
