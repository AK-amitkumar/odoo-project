# -*- coding: utf-8 -*-
{
    'name': "pbxmanager",
	'icon': "/pbxmanager/static/src/img/icon.png",

    'summary': """
        Provides PBX and ERP Integration""",

    'description': """
        Provides PBX and odoo ERP Integration have click to call, call pop up and call logs integration
    """,

    'author': "TechExtension",
    'website': "http://techextension.com/odoo-erp-pbx-asterisk-integration",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'pbx',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
		#'views/reports.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}