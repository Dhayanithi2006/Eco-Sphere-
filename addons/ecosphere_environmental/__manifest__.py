# -*- coding: utf-8 -*-
{
    'name': 'EcoSphere Environmental Management',
    'version': '18.0.1.0.0',
    'summary': 'Carbon ledger, versioned emission factors, and carbon target goals',
    'description': """
EcoSphere Environmental Management
==================================
This module implements the Environmental pillar of ESG for Odoo 18.

Key Features:
-------------
* Versioned Emission Factor registry.
* Carbon Transactions ledger tracking Scope 1, 2, and 3 activities.
* Department and Company carbon goals.
* Product footprint template parameters.
* Powered by a centralized calculations engine.
    """,
    'author': 'EcoSphere Team',
    'website': 'https://github.com/your-repo/eco-sphere',
    'category': 'Sustainability',
    'depends': [
        'ecosphere_base',
        'account',
        'mrp',
        'hr_expense',
        'fleet',
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/emission_factor_views.xml',
        'views/carbon_transaction_views.xml',
        'views/environmental_goal_views.xml',
        'views/product_views.xml',
        'views/menu_views.xml',
    ],
    'demo': [
        'data/demo_data.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
