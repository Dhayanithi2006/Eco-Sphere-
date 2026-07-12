# -*- coding: utf-8 -*-
{
    'name': 'EcoSphere AI Advisor',
    'version': '18.0.1.0.0',
    'summary': 'Simulated AI decision advisor and query history logs',
    'description': """
EcoSphere AI Advisor
====================
This module implements simulated/integrated AI advisory features for Odoo 18.

Key Features:
-------------
* Advisory Wizard fetching real-time dashboard figures.
* Advisory History logs with feedback (Like 👍 / Dislike 👎) controls.
* Complete write isolation for security (cannot write to core ERP parameters).
    """,
    'author': 'EcoSphere Team',
    'website': 'https://github.com/your-repo/eco-sphere',
    'category': 'Sustainability',
    'depends': [
        'ecosphere_notifications',
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/ai_history_views.xml',
        'views/ai_advisor_wizard_views.xml',
        'views/menu_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
