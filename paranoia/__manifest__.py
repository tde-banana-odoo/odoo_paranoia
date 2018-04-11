# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Paranoia',
    'version': '1.0',
    'category': 'Games',
    'complexity': 'easy',
    'description': """
Paranoia Base module
====================
    """,
    'depends': ['mail', 'portal'],
    'data': [
        'data/configuration_data.xml',
        'data/paranoia_data.xml',
        'views/paranoia_views.xml',
        'views/paranoia_portal_templates.xml',
        'security/ir.model.access.csv',
        'security/paranoia_security.xml',
    ],
    'demo': [
        'data/paranoia_demo.xml',
    ],
    'installable': True,
    'auto_install': False,
}
