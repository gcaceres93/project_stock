# -*- coding: utf-8 -*-
{
    'name': "rate_currencyBI",

    'summary': """
        Modulo Gestión de Tasa Monetario...
       """,

    'description': """
        Gestión de Tasas para el uso en los calculos del valor monetario de cada Pais 
    """,

    'author': "Sati",
    'website': "http://www.sati.com.py",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'module',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale','account'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/res_currency.xml',
        # 'views/templates.xml',
    ],
    # only loaded in demonstration mode
    # 'demo': [
    #     'demo/demo.xml',
    # ],
}
