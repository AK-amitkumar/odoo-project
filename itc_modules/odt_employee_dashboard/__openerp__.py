# -*- coding: utf-8 -*-
{
    'name': 'Employee Dashboard',
    'version': '1.1',
    'category': 'Hr',
    'sequence': 14,
    "author": "Odootec",
    'summary': 'dash board for employee.',
    'description': """
    Includes.\n
    1. Employee Form
    2. Request  Leave
    4. Payslip Analysis Report
    5. Leave analysis Report
    """,
    'website': "www.odootec.com",
    'depends': ['hr', 'hr_payroll', 'hr_holidays', 'l10n_in_hr_payroll'],
    'data': [
        # 'security/hr_employee_security.xml',
        # 'security/ir.model.access.csv',
        # 'views/hr_view.xml'

        ],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': True,
}
