#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest

from flask_styleguide import key


def test_append_extension_prefix_to_config_key():
    assert key('key').startswith('STYLEGUIDE')


def test_uppercase_config_key():
    assert key('template') == 'STYLEGUIDE_TEMPLATE'
