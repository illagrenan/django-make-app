================================================
Django Make App: *generate Django app from YAML*
================================================

.. image:: https://img.shields.io/pypi/v/django_make_app.svg
        :target: https://pypi.python.org/pypi/django_make_app
        :alt: PyPi

.. image:: https://img.shields.io/travis/illagrenan/django-make-app.svg
        :target: https://travis-ci.org/illagrenan/django-make-app
        :alt: TravisCI

.. image:: https://coveralls.io/repos/github/illagrenan/django-make-app/badge.svg?branch=master
        :target: https://coveralls.io/github/illagrenan/django-make-app?branch=master 
        :alt: Coverage

.. image:: https://requires.io/github/illagrenan/django-make-app/requirements.svg?branch=master
     :target: https://requires.io/github/illagrenan/django-make-app/requirements/?branch=master
     :alt: Requirements Status


Installation
------------

This package is not yet on PyPI. Supported Python versions are: ``2.7``, ``3.3``, ``3.4`` and ``3.5``.

.. code:: shell

    pip install --upgrade git+git://github.com/illagrenan/django-make-app.git#egg=django-make-app

Usage
-----

If you want generate app ``library``, create ``library.yaml`` in project root.

.. code:: yaml

    app_name: library
    models:
      - User:
        - name:char
        - email:char
      - Book:
        - library:fk
      - Library

Now execute:

.. code:: shell

    django-make-app generate library

This structure will be created for you:

.. code::

    LIBRARY
    │   admin.py
    │   api.py
    │   apps.py
    │   checks.py
    │   forms.py
    │   models.py
    │   receivers.py
    │   serializers.py
    │   signals.py
    │   urls.py
    │   views.py
    │   __init__.py
    │
    ├───management
    │   │   __init__.py
    │   │
    │   └───commands
    │           library_command.py
    │           __init__.py
    │
    ├───migrations
    │       __init__.py
    │
    ├───templates
    │   └───web
    │           book_delete.html
    │           book_detail.html
    │           book_form.html
    │           book_list.html
    │           library_delete.html
    │           library_detail.html
    │           library_form.html
    │           library_list.html
    │           user_delete.html
    │           user_detail.html
    │           user_form.html
    │           user_list.html
    │
    ├───templatetags
    │       web_tags.py
    │       __init__.py
    │
    └───tests
            factories.py
            test_book.py
            test_library.py
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
