#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    flask.ext.styleguide
    ~~~~~~~~~~~~~~~~~~~~

    A live Style Guide for your Flask application.

    :copyright: (c) 2014 by Vital Kudzelka <vital.kudzelka@gmail.com>
    :license: MIT
"""
import sys
import subprocess
from setuptools import setup
from setuptools import Command
from setuptools import find_packages


version = "0.1.1"


class pytest(Command):
    user_options = [
        ('coverage', None, 'report coverage')
    ]

    def initialize_options(self):
        self.coverage = None

    def finalize_options(self):
        pass

    def run(self):
        basecmd = [sys.executable, '-m', 'pytest']
        if self.coverage:
            basecmd += ['--cov', 'flaskext']
        errno = subprocess.call(basecmd + ['tests'])
        raise SystemExit(errno)


def get_file(filename):
    """Returns file content line by line."""
    try:
        with open(filename, 'r') as f:
            rv = f.readlines()
    except IOError:
        rv = []
    return rv


def get_long_description():
    readme = get_file('README')
    return ''.join(readme)


install_requires = get_file('requirements/main.txt')
tests_require = get_file('requirements/tests.txt')
extras_require = {
    'test': tests_require
}


setup(
    name='Flask-Styleguide',

    # Versions should comply with PEP440. For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # http://packaging.python.org/en/latest/tutorial.html#version
    version=version,

    author='Vital Kudzelka',
    author_email='vital.kudzelka@gmail.com',

    url="https://github.com/vitalk/flask-styleguide",
    description='A live Style Guide for your Flask application.',
    long_description=get_long_description(),
    license='MIT',

    packages=find_packages(exclude=['docs', 'tests']),
    zip_safe=False,
    platforms='any',
    install_requires=install_requires,
    extras_require=extras_require,
    tests_require=tests_require,
    test_suite='tests',
    cmdclass={
        'test': pytest,
    },

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
