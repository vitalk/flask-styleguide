#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Flask-Styleguide
================

Extension provides an easy way to automatically generate living styleguide
for your application from `KSS documentation <http://warpspire.com/kss/>`_
format.

What is KSS
-----------

KSS is a documentation for humans. It's human readable, machine parsable, and
easy to remember. `Learn the syntax in less then 5 minutes
<http://warpspire.com/kss/>`_.

Contributing
------------

Don't hesitate to create a `GitHub issue
<https://github.com/vitalk/flask-styleguide/issues>`_ for any **bug** or
**suggestion**.

Links
-----

* Documentation: http://flask-styleguide.readthedocs.org
* GitHub: https://github.com/vitalk/flask-styleguide
* PyPI: https://pypi.python.org/pypi/flask-styleguide
* Example: https://vitalk.github.io/flask-styleguide-example

"""
import io
import os
import re
import sys
import subprocess
from setuptools import setup
from setuptools import Command
from setuptools import find_packages


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
            basecmd += ['--cov', 'flask_styleguide']
        errno = subprocess.call(basecmd + ['tests'])
        raise SystemExit(errno)


def read(*parts):
    """Reads the content of the file created from *parts*."""
    try:
        with io.open(os.path.join(*parts), 'r', encoding='utf-8') as f:
            return f.readlines()
    except IOError:
        return []


def get_version():
    version_file = ''.join(read('flask_styleguide', '__init__.py'))
    version_match = re.search(r'^__version__ = [\'"]([^\'"]*)[\'"]',
                              version_file, re.MULTILINE)
    if version_match:
        return version_match.group(1)
    raise RuntimeError('Unable to find version string.')


__version__ = get_version()
install_requires = read('requirements', 'main.txt')
tests_require = read('requirements', 'tests.txt')
extras_require = {
    'test': tests_require
}


setup(
    name='Flask-Styleguide',
    version=__version__,

    author='Vital Kudzelka',
    author_email='vital.kudzelka@gmail.com',

    url="https://github.com/vitalk/flask-styleguide",
    description='A living Styleguide for your Flask application.',
    download_url='https://github.com/vitalk/flask-styleguide/tarball/%s' % __version__,
    long_description=__doc__,
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

    keywords='flask live styleguide',
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Framework :: Flask',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
