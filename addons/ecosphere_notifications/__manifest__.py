# -*- coding: utf-8 -*-
{
    'name': 'EcoSphere Notification Engine',
    'version': '18.0.1.0.0',
    'summary': 'Alert definitions, mail templates, and threshold breach triggers',
    'description': """
EcoSphere Notification Engine
=============================
This module handles automated alarms and messaging configurations for EcoSphere.

Key Features:
-------------
* Centralized Alerts model (`ecosphere.notification`).
* Mail Templates for Carbon Goal breaches and Compliance violations.
* Automated override hooks checking thresholds on database modifications.
    """,
    'author': 'EcoSphere Team',
    'website': 'https://github.com/your-repo/eco-sphere',
    'category': 'Sustainability',
    'depends': [
        'ecosphere_dashboard',
        'mail',
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/mail_templates.xml',
        'views/notification_views.xml',
        'views/menu_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
