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
    'depends': ['base','mail'],
    'data': [
        'data/ir_module_category_data.xml',
        'data/report_paperformat_data.xml',
        'security/res_groups.xml',
        'report/plate_pdf.xml',
        'security/ir.model.access.csv',
        'views/property_details_views.xml',
        'views/dashboard.xml',
        'views/zone_views.xml',
        'views/ward_views.xml',
        'views/property_type_views.xml',
        'views/menuitems.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'smkc/static/src/components/**/*.js', 
            'smkc/static/src/components/**/*.xml',
            # 'smkc/static/src/js/dashboard.js', 

            # 'smkc/static/src/xml/dashboard.xml',

        ],
    },

    'installable': True,
    'application': True,
}



