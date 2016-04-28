# coding=utf-8

import io

from setuptools import setup

setup(
    name='django_make_app',
    version='0.1.2.1',
    description='Define models and fields using YAML and generate app for Django with views, forms, templates etc.',
    long_description=io.open('README.rst').read(),
    url='https://github.com/illagrenan/django-make-app',
    license='MIT',
    author='Vasek Dohnal',
    author_email='vaclav.dohnal@gmail.com',
    packages=['django_make_app'],
    install_requires=[
        'pyaml',
        'jinja2',
        'yapf',
        'glob2',
        'isort',
        'click'
    ],
    entry_points={
        'console_scripts': [
            'django-make-app=django_make_app.runner:cli'
        ],
    },
    include_package_data=True,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=[]
)
