#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of flask-paypal.
# https://github.com/heynemann/flask-paypal

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Bernardo Heynemann <heynemann@gmail.com>

from setuptools import setup, find_packages
from flask_paypal import __version__

tests_require = [
    'mock',
    'nose',
    'coverage',
    'yanc',
    'preggy',
    'tox',
    'ipdb',
    'coveralls',
    'sphinx',
]

setup(
    name='flask-paypal',
    version=__version__,
    description='Flask integration with PayPal, mainly focused on subscriptions.',
    long_description='''
Flask integration with PayPal, mainly focused on subscriptions.
''',
    keywords='paypal payment subscription flask jinja',
    author='Bernardo Heynemann',
    author_email='heynemann@gmail.com',
    url='https://github.com/heynemann/flask-paypal',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: Unix',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Operating System :: OS Independent',
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'paypalrestsdk>=1.11.0,<1.12.0',
    ],
    extras_require={
        'tests': tests_require,
    },
    entry_points={
        'console_scripts': [
            # add cli scripts here in this form:
            # 'flask-paypal=flask_paypal.cli:main',
        ],
    },
)
