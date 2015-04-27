#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    flask_styleguide.core
    ~~~~~~~~~~~~~~~~~~~~~

    Core module of the extension.

    :copyright: (c) 2014 by Vital Kudzelka <vital.kudzelka@gmail.com>
    :license: MIT
"""
import os
from pykss import Parser
from werkzeug.datastructures import ImmutableDict

from .jinjaext import StyleguideExtension


default_options = ImmutableDict({
    # The path to template uses to render styleguide section.
    'template_name': 'styleguide/section.html',
})


key = lambda name: ('styleguide_%s' % name).upper()
"""Returns config key name with extension prefix."""


class Styleguide(object):

    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """Register required jinja extension to application.

        :param app: The :class:`Flask` instance to init.
        """
        for name, value in default_options.items():
            app.config.setdefault(key(name), value)

        paths = get_static_paths(app)
        if not paths:
            app.logger.warn(
                "Looks like neither your application or "
                "none of the application blueprints is not properly "
                "configured to serve static files."
            )

        app.jinja_env.add_extension(StyleguideExtension)
        app.jinja_env.styleguide_kss_parser = Parser(*paths)
        app.jinja_env.styleguide_template_name = app.config[key('template_name')]


def get_static_paths(app):
    """Return the list of static folders for an application and
    blueprints registered on it.

    :param app: The :class:`Flask` instance to inspect.
    """
    paths = []
    for app_or_bp in [app] + app.blueprints.values():
        if app_or_bp.has_static_folder:
            paths.append(app_or_bp.static_folder)
            continue

        # Older Flask versions (<0.7) does not support custom static folder,
        # so check the fixed one.
        if not hasattr(app_or_bp, 'static_folder'):
            paths.append(os.path.join(app_or_bp.root_path, 'static'))

    return sorted(set(paths))
