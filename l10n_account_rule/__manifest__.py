# -*- coding: utf-8 -*-
{
    "name": "Fiscal Account Rule",

    'version': '19.0.0.0',

    'summary': """Fiscal Account Rule""",

    'description': """Fiscal Account Rule""",

    'category': 'all',

    'author': "Odoo",

    'website': 'https://odoo.com',

    "depends": ['base', 'stock', 'sale', 'sale_management', 'purchase', 'account', 'hr'],

    "data": [
        'security/ir.model.access.csv',
        'data/sequence_data.xml',
        'views/product_brand_views.xml',
        'views/engine_numer_views.xml',
        'views/sale_order_views.xml',
        'views/product_template_views.xml',
        'views/product_product_views.xml',
        'views/purchasde_order_views.xml',
        'views/res_partner_views.xml',
        'views/account_move_views.xml',
        'views/emp_perform_tracking_views.xml',
    ],

}

