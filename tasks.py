# -*- encoding: utf-8 -*-
# ! python2

from __future__ import (absolute_import, division, print_function, unicode_literals)

import shutil

from invoke import run, task


@task
def clean_build():
    shutil.rmtree('django_make_app.egg-info', ignore_errors=True)
    shutil.rmtree('build', ignore_errors=True)
    shutil.rmtree('dist', ignore_errors=True)
    shutil.rmtree('__pycache__', ignore_errors=True)


@task
def lint():
    run("flake8 django_make_app tests")


@task
def test():
    run("py.test --verbose --showlocals --cov=django_make_app tests/")


@task
def test_setuptools():
    run("python setup.py test")


@task
def test_nosetests():
    run("python setup.py nosetests -v --with-doctest")


@task
def test_all():
    run("tox")


@task
def coverage():
    run("coverage run --source django_make_app setup.py test")
    run("coverage report -m")
    run("coverage html")


@task
def install_requirements():
    run("pip install -r requirements.txt --upgrade --use-wheel")


@task
def test_install():
    run("pip uninstall django_make_app --yes", warn=True)

    run("pip install --use-wheel --no-index --find-links dist django_make_app")
    run("pip uninstall django_make_app --yes")


@task
def build():
    run("python setup.py check --verbose --strict --restructuredtext")

    run("python setup.py build")
    run("python setup.py sdist")
    run("python setup.py bdist_wheel")


@task
def publish():
    run('python setup.py sdist upload -r pypi')
    run('python setup.py bdist_wheel upload -r pypi')
