# -*- coding: utf-8 -*-
{
    'name': 'EcoSphere Base',
    'version': '18.0.1.0.0',
    'summary': 'Core foundation, RBAC security groups and settings for EcoSphere sustainability platform',
    'description': """
EcoSphere Base Module
======================
This module establishes the foundational data structures and Role-Based Access Controls (RBAC)
for the EcoSphere Enterprise Sustainability Intelligence Platform.

Key Features:
-------------
* Extends users, companies, and departments with ESG parameters.
* Defines security groups for Employees, Managers, Auditors, Compliance Officers, and Administrators.
* Configures record-level access isolation rules for departments.
* Provides global configuration parameters for sustainability settings.
    """,
    'author': 'EcoSphere Team',
    'website': 'https://github.com/your-repo/eco-sphere',
    'category': 'Sustainability',
    'depends': [
        'base',
        'hr',
        'mail',
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/res_config_settings_views.xml',
        'views/res_users_views.xml',
        'views/hr_department_views.xml',
        'views/menu_views.xml',
    ],
    'demo': [
        'data/demo_data.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
