Getting started
---------------

Use default Flask API to initialize application and bound it to application
object::

    from flask import Flask
    from flask_styleguide import Styleguide

    app = Flask(__name__)
    styleguide = Styleguide(app)

Define endpoint for your styleguide in application or blueprint::

    @app.route('/styleguide/')
    def styleguide():
        return render_template('styleguide.html')

The new jinja tag ``styleguide`` becomes available when extension is
initialized, so it's easy to scaffold your styleguide:

.. code-block:: html+jinja

    {% extends 'layout.html' %}
    {% block main %}
      {% styleguide "2.1" %}
        <button class="button$modifier_class">Button</button>
        <a class="button$modifier_class">A button link</a>
      {% endstyleguide %}
    {% endblock %}


.. note::

    The ``styleguide/section.html`` template will be used for each section in
    your styleguide (like ``2.1`` in the example above). You are free to
    define you own template or reuse this one:

    .. code-block:: html+jinja

        <article class="style-guide" id="{{ section.section }}">
          <h4 class="style-guide-reference">{{ section.section }}</h4>

          <div class="style-guide-description">
            <p>{{ section.description|safe }}</p>
            {% if section.modifiers %}
              <ul class="style-guide-modifiers">
                {% for m in section.modifiers %}
                  <li><strong>{{ m.name }}</strong> - {{ m.description }}</li>
                {% endfor %}
              </ul>
            {% endif %}
          </div>

          <div class="style-guide-element">
            {{ section.example|safe }}
          </div>

          {% for m in section.modifiers %}
            <div class="style-guide-element">
              <small class="style-guide-modifier">{{ m.name }}</small>
              {{ m.example|safe }}
            </div>
          {% endfor %}

          <div class="style-guide-html">
            <pre>{{ section.example|forceescape }}</pre>
          </div>
        </article>

Depending on the template you are using, apply some styles to it.

.. note::

    This example uses `less <http://lesscss.org>`_ and can be installed via
    `bower <http://bower.io>`_:

    .. code-block:: sh

        bower install --save classy-style-guide

    .. code-block:: css

        @import 'classy-style-guide/components.style-guide.less';
