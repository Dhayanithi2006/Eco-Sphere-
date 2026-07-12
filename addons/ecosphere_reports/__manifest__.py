# -*- coding: utf-8 -*-
{
    'name': 'EcoSphere ESG Reports',
    'version': '18.0.1.0.0',
    'summary': 'Printable QWeb PDF reports and structured data export wizards for ESG metrics',
    'description': """
EcoSphere ESG Reports
=====================
This module manages compilation layouts and data extractions for the EcoSphere platform.

Key Features:
-------------
* Printable QWeb PDF reports (Environmental Summary & Executive ESG Brief).
* Transient wizard supporting date-filtered and department-filtered CSV exports.
* Clean tabular document formats containing ESG summaries.
    """,
    'author': 'EcoSphere Team',
    'website': 'https://github.com/your-repo/eco-sphere',
    'category': 'Sustainability',
    'depends': [
        'ecosphere_environmental',
        'ecosphere_social',
        'ecosphere_governance',
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'reports/report_actions.xml',
        'reports/template_environmental.xml',
        'reports/template_esg_executive.xml',
        'views/export_wizard_views.xml',
        'views/menu_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
