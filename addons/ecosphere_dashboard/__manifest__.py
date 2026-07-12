# -*- coding: utf-8 -*-
{
    'name': 'EcoSphere Sustainability Dashboard',
    'version': '18.0.1.0.0',
    'summary': 'Central KPI engine and modular dashboard widgets',
    'description': """
EcoSphere Sustainability Dashboard
==================================
This module provides the central metrics dashboard for the EcoSphere platform.

Key Features:
-------------
* Centralized KPI Engine calculating E, S, G, and overall weighted ESG scores.
* Transient Dashboard model serving real-time statistics.
* Beautiful full-width metric card form layout.
    """,
    'author': 'EcoSphere Team',
    'website': 'https://github.com/your-repo/eco-sphere',
    'category': 'Sustainability',
    'depends': [
        'ecosphere_reports',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/dashboard_views.xml',
        'views/menu_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
