# -*- coding: utf-8 -*-
{
    'name': 'EcoSphere Gamification Management',
    'version': '18.0.1.0.0',
    'summary': 'Challenges, employee point histories, rewards, and leaderboards',
    'description': """
EcoSphere Gamification Management
=================================
This module implements the Gamification & Employee Engagement features for Odoo 18.

Key Features:
-------------
* Trophies & Badges Cabinet.
* Sustainability Challenge campaigns (e.g. Zero-Waste campaigns).
* Points Ledger and log histories tracking employee contributions.
* Rewards catalog and redemption validation store.
* Dynamic Leaderboard sorted by ESG points.
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
        'views/badge_views.xml',
        'views/challenge_views.xml',
        'views/reward_views.xml',
        'views/leaderboard_views.xml',
        'views/menu_views.xml',
    ],
    'demo': [
        'data/demo_data.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
