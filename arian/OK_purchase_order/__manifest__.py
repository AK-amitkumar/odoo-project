# -*- coding: utf-8 -*-
{
    'name': "Purchase Order",

    'summary': "Purchase Order original report modification",

    'description': "Purchase Slip original report modification",

    'author': "Muhammmad Awais",
    'website': "http://www.bcube.com",

    # any module necessary for this one to work correctly
    'depends': ['purchase','stock'],
    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'templates.xml',
    ],
}