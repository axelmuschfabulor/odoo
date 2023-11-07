# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'Estate',
    'version': '1.0',
    'category': 'Sales/CRM',
    'sequence': 15,
    'summary': 'Track leads and close opportunities',
    'website': 'https://www.odoo.com/app/crm',
    'depends': [
        'base'
    ],
    'data': [
        'security/ir.model.access.csv',

        'views/estate_property_views.xml',
        'views/estate_menus.xml',
    ],
    'demo': [
       
    ],
    'installable': True,
    'application': True,

    'license': 'LGPL-3',
}
