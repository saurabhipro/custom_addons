{
    'name': 'Tax Transaction Tracker',
    'version': '18.0.1.0.0',
    'category': 'Accounting/Taxes',
    'summary': 'Track tax transactions and payments',
    'description': """
        This module helps track tax transactions including:
        * Tax payment records
        * Different types of taxes
        * Payment dates and deadlines
        * Transaction history
        * Tax payment status
    """,
    'author': 'Your Company',
    'website': 'https://www.yourcompany.com',
    'depends': ['base', 'account'],
    'data': [
        'security/tax_tracker_security.xml',
        'security/ir.model.access.csv',
        'views/tax_transaction_views.xml',
        'views/tax_type_views.xml',
        'views/menus.xml',
        'data/tax_type_data.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
