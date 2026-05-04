# -*- coding: utf-8 -*-
{
    'name': "Stock Dynamic Report",

    'version': '19.0.0.0',

    'summary': """ Stock Dynamic Report """,

    'description': """ Stock Dynamic Report """,

    'category': 'all',

    'author': "Odoo",

    'website': 'https://odoo.com',

    'depends': ['base', 'sale', 'stock', 'purchase', 'account'],

    'data': [
        'security/ir.model.access.csv',
        'wizard/stock_aging_report_wiz_view.xml',
        'reports/reports.xml',
        'reports/custom_quotation_report_template.xml',
        'reports/internal_so_quotation_report_template.xml',
        'reports/purchase_order_report_template.xml',
        'reports/goods_reciept_note_report_template.xml',
        'reports/credit_note_report_template.xml',
        'reports/custom_invoice_report_template.xml',
        'reports/custom_do_report_template.xml',
    ],

}

