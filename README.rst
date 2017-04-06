================================================
Django Make App: *generate Django app from YAML*
================================================

.. image:: https://badge.fury.io/py/django_make_app.svg
        :target: https://pypi.python.org/pypi/django_make_app
        :alt: PyPi

.. image:: https://img.shields.io/badge/license-MIT-blue.svg
        :target: https://pypi.python.org/pypi/django_make_app/
        :alt: MIT

.. image:: https://api.travis-ci.org/illagrenan/django-make-app.svg
        :target: https://travis-ci.org/illagrenan/django-make-app
        :alt: TravisCI

.. image:: https://coveralls.io/repos/github/illagrenan/django-make-app/badge.svg?branch=master
        :target: https://coveralls.io/github/illagrenan/django-make-app?branch=master
        :alt: Coverage

.. image:: https://requires.io/github/illagrenan/django-make-app/requirements.svg?branch=master
     :target: https://requires.io/github/illagrenan/django-make-app/requirements/?branch=master
     :alt: Requirements Status

Introduction
------------

Django-make-app will generate code of your Django app from a simple YAML schema. This is similar to ``manage.py startapp`` but much powerful.

This will be generated from models definitions:

- Admin classes and admin forms
- Django REST framework View Sets, Serializers and Router configuration
- Django AppConfig
- Django System Checks
- Forms classes
- Models classes
- Detail/Delete/Update/Create/List views, urls and templates
- Management command example
- Dummy filter
- Signals and receivers files
- TODO tests

Installation
------------

Supported Python versions are: ``2.7``, ``3.4``, ``3.5``, ``3.6``, ``pypy`` and ``pypy3``.

.. code:: shell

    pip install --upgrade django-make-app

Python ``3.3`` is not supported due to incompatibility of yapf (see: https://github.com/google/yapf#python-versions). If you're on Python
``3.3``, you can use this package with option ``django-make-app generate ... --no-optimize`` (this will skip yapf).

Usage
-----

If you want to generate app called ``library``, create a file ``app_schema.yaml`` in project's root and define models:

.. code:: yaml

    apps:
        -
            name: library           # all files will be generated into library/ directory (will be created)
            models:
              - User:               # model name
                - name:char         # model field "name" of type "char"
                - email:char        # model field "email" of type "char"
              - Book:               # another model
                - library:fk        # model field "library" of type "foreign key" to "library"
              - Article             # empty model without fields
        -
            name: my_another_awesome_app
            models:
                - City
                - Country

You can also print example configuration by executing (or check `templates/example.yaml <https://github.com/illagrenan/django-make-app/blob/master/django_make_app/templates/example.yaml>`__):

.. code:: shell

    django-make-app write_config > app_schema.yaml

Finally to generate source code of your app, execute:

.. code:: shell

    django-make-app generate library

This structure will be generated:

.. code::

    LIBRARY
    |   admin.py
    |   api.py
    |   apps.py
    |   checks.py
    |   forms.py
    |   models.py
    |   receivers.py
    |   serializers.py
    |   signals.py
    |   urls.py
    |   views.py
    |   __init__.py
    |
    |---management
    |   |   __init__.py
    |   |
    |   \---commands
    |           library_command.py
    |           __init__.py
    |
    |---migrations
    |       __init__.py
    |
    |---templates
    |   \---web
    |           book_delete.html
    |           book_detail.html
    |           book_form.html
    |           book_list.html
    |           article_delete.html
    |           article_detail.html
    |           article_form.html
    |           article_list.html
    |           user_delete.html
    |           user_detail.html
    |           user_form.html
    |           user_list.html
    |
    |---templatetags
    |       web_tags.py
    |       __init__.py
    |
    \---tests
            factories.py
            test_book.py
            test_article.py
            test_user.py
            __init__.py


Inspiration
-----------

- https://github.com/mmcardle/django_builder

License
-------

The MIT License (MIT)

Copyright (c) 2016 Vašek Dohnal

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
