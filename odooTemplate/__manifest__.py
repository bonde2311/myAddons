# -*- coding: utf-8 -*-
{
    'name': 'Legel Document Initiations',
    'version': '1.0',
    'summary': 'Brief description of the module',
    'description': '''
        Detailed description of the module
    ''',
    'category': 'Uncategorized',
    'author': 'Cybrosys Techno Solutions',
    'company': 'Cybrosys Techno Solutions',
    'maintainer': 'Cybrosys Techno Solutions',
    'website': 'https://www.cybrosys.com',
    'depends': ['base', 'mail'],
    'data': [
        'data/sequence.xml',
        'security/security.xml',
        'security/company_master_rule.xml',
        'security/ir.model.access.csv',
        'views/legel_document_initiations_views.xml',
        'views/company_master.xml',
        'views/custom_partner.xml',
        'views/requester.xml',
        'views/res_users_view.xml',
        'views/document_type.xml',
    ],
    'license': 'LGPL-3',
    'installable': True,
    'application': False,
    'auto_install': False,
}