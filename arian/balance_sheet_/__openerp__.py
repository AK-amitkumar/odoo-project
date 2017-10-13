# -*- coding: utf-8 -*-

{
    'name': "Balance Sheet UFC",

    'summary': "Balance Sheet UFC",

    'description': "Balance Sheet UFC",

    'author': "Muhammmad Kamran",
    'website': "http://www.bcube.com",

    # any module necessary for this one to work correctly
    'depends': ['base', 'report','account','report_structure_module'],
    # always loaded
    'data': [
        'template.xml',
        'views/module_report.xml',
    ],
    'css': ['static/src/css/report.css'],
}