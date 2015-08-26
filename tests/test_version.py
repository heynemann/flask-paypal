#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of flask-paypal.
# https://github.com/heynemann/flask-paypal

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Bernardo Heynemann <heynemann@gmail.com>

from preggy import expect

from flask_paypal import __version__
from tests.base import TestCase


class VersionTestCase(TestCase):
    def test_has_proper_version(self):
        expect(__version__).to_equal('0.1.0')
