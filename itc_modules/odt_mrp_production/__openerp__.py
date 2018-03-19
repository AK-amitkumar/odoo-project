# -*- coding: utf-8 -*-
{
    'name': "odt_mrp_production",

    'summary': """ manufacturing order cancel
     """,

    'description': """
        Manage user to delete manufacturing order in any case rather in
        case Done
    """,

    'author': "odootec",
    'website': "http://www.odootec.com",


    'category': 'Manufacturing',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','mrp',"stock"],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        # 'views/mrp_production.xml',
    ],

}