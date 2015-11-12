Changelog
---------

0.4.0
~~~~~

- Add documentation.

0.3.0
~~~~~

- Add missed files into source distribution.

- Remove executable bit from py files.

- Refactor test suite; use pytest-flask for testing.

0.2.0
~~~~~

- Set package status to beta :tada:

- Add styleguide example into readme (#5).

- Fix python 2.6 and python 3 compatibility.

- Add compatible python versions into package metadata.

0.1.5
~~~~~

- Use `flask_styleguide` instead of `flask.ext.styleguide` in package imports
  since the `import flask.ext.foo` syntax is being deprecated for Flask 1.0,
  as per mitsuhiko/flask#1135.

0.1.4
~~~~~

- Replace deprecated ``codecs.open`` with ``io.open``.

0.1.3
~~~~~

- Parse package at runtime to get version string, as per #6.

0.1.2
~~~~~

- Ensure the html examples has no extra leading whitespaces by dedenting them
  during render.

0.1.1
~~~~~

- First release on PyPi.

0.1.0
~~~~~

- Proof of concept.
