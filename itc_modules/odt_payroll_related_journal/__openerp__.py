# -*- coding: utf-8 -*-
{
    'name': "contributer register",

    'summary': """
    Salary Rule
        """,

    'description': """
Customize in view of hr.contribution.register Model show partner_id field
    """,

    'author': "Your Company",
    'website': "http://www.odootec.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'hr_payroll'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        # 'view/payroll_register_id_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [

    ],
}
