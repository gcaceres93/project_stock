# -*- coding: utf-8 -*-
{
'name': 'Project Stock',
'version': '1.0',
'category': 'Update',
'description': """Module for integrate sales, project and stock.
""",
'author': 'Rapidsoft',
'website': 'http://www.rapidsoft.com.py',
'depends': ['base','project','stock','sale'],
'data': [
        'views/sale_view.xml',
        'views/stock_view.xml',
        'views/project_view.xml',
        'security/security.xml',
        'security/ir.model.access.csv'
        ],

'installable': True,
    'auto_install': False,
    'application': True,

}
