#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    flask_styleguide
    ~~~~~~~~~~~~~~~~

    A live Style Guide for your Flask application.

    :copyright: (c) 2014 by Vital Kudzelka <vital.kudzelka@gmail.com>
    :license: MIT
"""
# Versions should comply with PEP440. For a discussion on single-sourcing
# the version across setup.py and the project code, see
# http://packaging.python.org/en/latest/tutorial.html#version
__version__ = '0.1.5'


from .core import key
from .core import Styleguide
from .core import get_static_paths
