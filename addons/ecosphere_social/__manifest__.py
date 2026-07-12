# -*- coding: utf-8 -*-
{
    'name': 'EcoSphere Social Management',
    'version': '18.0.1.0.0',
    'summary': 'CSR programs, volunteer hour logs, training registries, and diversity analytics',
    'description': """
EcoSphere Social Management
===========================
This module implements the Social pillar of ESG for Odoo 18.

Key Features:
-------------
* CSR Activity campaigns.
* Volunteer Hour logs submitted by employees and approved by managers.
* Automatic ESG Point rewards allocation for employees.
* Diversity registers at the departmental level.
* Sustainability training registers and participant completion analytics.
    """,
    'author': 'EcoSphere Team',
    'website': 'https://github.com/your-repo/eco-sphere',
    'category': 'Sustainability',
    'depends': [
        'ecosphere_base',
        'ecosphere_environmental',
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/csr_activity_views.xml',
        'views/csr_participation_views.xml',
        'views/training_views.xml',
        'views/diversity_dashboard_views.xml',
        'views/menu_views.xml',
    ],
    'demo': [
        'data/demo_data.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
