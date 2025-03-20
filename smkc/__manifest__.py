# -*- coding: utf-8 -*-
{
    'name': "smkc",
    'summary': "Short (1 phrase/line) summary of the module's purpose",
    'description': """
        Long description of module's purpose
    """,
    'author': "Anjli Odoo Developer",
    'website': "",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base'],
    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/property_details_views.xml',
        'views/zone_views.xml',
        'views/ward_views.xml',
        'views/property_type_views.xml',
        'views/menuitems.xml',
    ],


    'installable': True,
    'application': True,
}



