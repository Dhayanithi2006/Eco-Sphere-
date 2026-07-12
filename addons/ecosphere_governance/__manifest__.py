# -*- coding: utf-8 -*-
{
    'name': 'EcoSphere Governance Management',
    'version': '18.0.1.0.0',
    'summary': 'Compliance policies, acknowledgments, audits, issues, and risk registers',
    'description': """
EcoSphere Governance Management
===============================
This module implements the Governance pillar of ESG for Odoo 18.

Key Features:
-------------
* Policies document management with approval workflow.
* Automatic employee policy sign-off propagation.
* Scheduled audits tracking with compliance outcomes.
* Compliance issue logs and priority tracking.
* Risk Register with likelihood/impact score engine.
    """,
    'author': 'EcoSphere Team',
    'website': 'https://github.com/your-repo/eco-sphere',
    'category': 'Sustainability',
    'depends': [
        'ecosphere_base',
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/policy_views.xml',
        'views/policy_acknowledgment_views.xml',
        'views/audit_views.xml',
        'views/compliance_issue_views.xml',
        'views/risk_views.xml',
        'views/menu_views.xml',
    ],
    'demo': [
        'data/demo_data.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
