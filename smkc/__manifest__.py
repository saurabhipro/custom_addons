# -*- coding: utf-8 -*-
{
    'name': 'SMKC',
    'summary': """
        Property Survey Management System for Suryabinayak Municipality
    """,
    'description': """
        Property Survey Management System for Suryabinayak Municipality
    """,
    'author': 'Windsurf',
    'website': 'https://www.windsurf.io',
    'category': 'Services/Property',
    'version': '0.1',
    'depends': ['base', 'mail', 'web'],
    'data': [
        # Security
        'security/ir.model.access.csv',
        
        
        # Views
        'views/zone_views.xml',
        'views/ward_views.xml',
        'views/property_type_views.xml',
        'views/property_details_views.xml',
        'views/property_details_template.xml',
        'views/property_map_view.xml',
        'views/res_users_views.xml',
        'views/mobile_otp_views.xml',
        'views/jwt_token_views.xml',
        'views/property_survey.xml',
        'views/dashboard.xml',
        'views/menuitems.xml',  # Load menus last
        # 'views/assets.xml',
    ],
    'assets': {
        'web.assets_backend': [
            # Components
            'smkc/static/src/components/kpi_card/kpi_card.js',
            'smkc/static/src/components/kpi_card/kpi_card.xml',
            'smkc/static/src/components/google_map/property_map.js',
            'smkc/static/src/components/google_map/property_map_template.xml',
            'smkc/static/src/components/dashboard/dashboard.js',
            'smkc/static/src/components/dashboard/dashboard.xml',
            'smkc/static/src/components/dashboard/dashboard.scss',
            'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css',
            'https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY&callback=Function.prototype',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
}
