# -*- coding: utf-8 -*-
{
    'name': "Sale Order",

    'summary': "Sale Order original report modification",

    'description': "Sale Slip original report modification",

    'author': "Muhammmad Awais",
    'website': "http://www.bcube.com",

    # any module necessary for this one to work correctly
    'depends': ['purchase','stock','sale'],
    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'templates.xml',
    ],
}