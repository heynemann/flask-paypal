#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of flask-paypal.
# https://github.com/heynemann/flask-paypal

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Bernardo Heynemann <heynemann@gmail.com>

from datetime import datetime, timedelta

from flask import Blueprint, current_app, g
from paypalrestsdk import configure, BillingPlan, BillingAgreement

from flask_paypal.version import __version__  # NOQA


mod = Blueprint('flask_paypal', __name__)


def init_app(app):
    app.register_blueprint(mod)

    if not app.config.get('PAYPAL_MODE', None):
        raise RuntimeError('You must specify the PAYPAL_MODE to use for transactions. Possible values are: "sandbox" or "live"')

    if not app.config.get('PAYPAL_CLIENT_ID', None) or not app.config.get('PAYPAL_CLIENT_SECRET'):
        raise RuntimeError('You must specify your pair of credentials for PayPal in PAYPAL_CLIENT_ID and PAYPAL_CLIENT_SECRET')

    if not app.config.get('PAYPAL_PLANS', None):
        raise RuntimeError('You must specify your subscription plans in PAYPAL_PLANS configuration')

    configure({
        "mode": app.config['PAYPAL_MODE'],
        "client_id": app.config['PAYPAL_CLIENT_ID'],
        "client_secret": app.config['PAYPAL_CLIENT_SECRET']
    })

    app.paypal = {
        'plans': {}
    }
    app.jinja_env.filters['plan_payment_url'] = plan_payment_url

    ensure_plans_activated(app)


def ensure_plans_activated(app):
    for plan_key, plan_data in app.config['PAYPAL_PLANS'].items():
        created_plan = create_plan(plan_data)
        app.paypal['plans'][plan_key] = activate_plan(created_plan.id)


def create_plan(plan):
    billing_plan_attributes = {
        "name": plan['name'],
        "description": plan.get('description', ''),
        "merchant_preferences": {
            "auto_bill_amount": plan.get('auto_bill_amount', True) and 'yes' or 'no',
            "cancel_url": plan.get('cancel_url', None),
            "initial_fail_amount_action": "continue",
            "max_fail_attempts": "1",
            "return_url": plan.get('return_url'),
            "setup_fee": {
                "currency": plan.get('setup_fee_currency', 'USD'),
                "value": plan.get('setup_fee_amount', 0.00)
            }
        },
        "payment_definitions": [
            {
                "amount": {
                    "currency": plan.get('plan_currency', 'USD'),
                    "value": plan.get('plan_amount')
                },
                "cycles": plan.get('cycles', 0),
                "frequency": plan.get('frequency_unit', 'MONTH'),
                "frequency_interval": plan.get('frequency_value', 1),
                "name": plan.get('payment_name', 'Regular'),
                "type": plan.get('payment_type', 'REGULAR'),
            }
        ],
        "type": plan.get('type', 'INFINITE')
    }

    billing_plan = BillingPlan(billing_plan_attributes)

    if billing_plan.create():
        return billing_plan
    else:
        raise RuntimeError(billing_plan.error)


def activate_plan(plan_id):
    billing_plan = BillingPlan.find(plan_id)
    if not billing_plan.activate():
        raise RuntimeError(billing_plan.error)

    return billing_plan


def plan_payment_url(value):
    plan_details = current_app.paypal['plans'][value]

    billing_agreement = BillingAgreement({
        "name": g.user.name,
        "description": "Agreement for %s" % plan_details['name'],
        "start_date": (datetime.utcnow() + timedelta(minutes=1)).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "plan": {
            "id": plan_details.id
        },
        "payer": {
            "payment_method": "paypal"
        },
    })
    import ipdb; ipdb.set_trace()  # XXX BREAKPOINT
    if billing_agreement.create():
        for link in billing_agreement.links:
            if link.rel == "approval_url":
                approval_url = link.href

                return approval_url

    raise RuntimeError('Could not get approval url for plan %s.' % plan_details.name)
