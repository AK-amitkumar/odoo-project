# -*- coding: utf-8 -*-
#
# Odootec <http://www.odootec.com>, Copyright (C) 2015 - Today.
#
# This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from openerp.report import report_sxw
from openerp import api, models
from datetime import timedelta, datetime


class HrPayslipParser(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context=None):
        super(HrPayslipParser, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'get_data': self._get_data,
        })
        self.context = context
        self.from_date = ''
        self.to_date = ''
        self.employee_ids = False
        self.salary_rule_ids = False


    def _get_data(self, data):
        cr = self.cr
        self.from_date = data['form']['start_date']
        self.to_date = data['form']['end_date']
        self.employee_ids = data['form']['employee_ids']
        self.salary_rule_ids = data['form']['salary_rule_ids']
        column_headings = self._get_salary_rule_names()
        data, payrule_total = self._get_table_data()
        total_list = ['Total', ' ']
        for rule in self.salary_rule_ids:
            total_list.append(payrule_total.get(rule, 0.0))
        res = {'column_headings': column_headings,
               'data': data,
               'total': total_list
        }
        return res

    def _get_salary_rule_names(self):
        rules = self.pool.get('hr.salary.rule').browse(self.cr, self.uid, self.salary_rule_ids)
        rule_names = ['Employee', 'Payslip Name']
        for rule in rules:
            rule_names.append(rule.code)
        return rule_names

    def _get_table_data(self):
        payslip_obj = self.pool.get('hr.payslip')
        employee_obj = self.pool.get('hr.employee')
        payslip_line_obj = self.pool.get('hr.payslip.line')
        data = []
        payrule_total = {}
        for employee in self.employee_ids:
            employ = employee_obj.browse(self.cr, self.uid, employee)

            payslip_ids = payslip_obj.search(self.cr, self.uid, [('employee_id', '=', employee),
                                                                 ('date_from', '<=', self.to_date),
                                                                 ('date_from', '>=', self.from_date)])
            if not payslip_ids:
                continue
            for payslip in payslip_ids:
                payslip_rec = payslip_obj.browse(self.cr, self.uid, payslip)
                data_list = [employ.name, payslip_rec.name]
                payslip_lines_ids = payslip_line_obj.search(self.cr, self.uid,[('slip_id', '=', payslip)])
                if not payslip_lines_ids:
                    continue
                for rule_id in self.salary_rule_ids:
                    rule_found = False
                    for payslip_lines_id in payslip_lines_ids:
                        payslip_line_rec = payslip_line_obj.browse(self.cr, self.uid, payslip_lines_id)
                        if payslip_line_rec.salary_rule_id.id == rule_id:
                            data_list.append(payslip_line_rec.total)
                            rule_found = True
                            if payrule_total.has_key(rule_id):
                                payrule_total[rule_id] += payslip_line_rec.total
                            else:
                                payrule_total[rule_id] = payslip_line_rec.total
                    if not rule_found:
                        data_list.append(0.00)
                data.append(data_list)
        return data, payrule_total

class HrPayslipReport(models.AbstractModel):
    _name = 'report.odootec_payslip_report.hr_payslip_report'
    _inherit = 'report.abstract_report'
    _template = 'odootec_payslip_report.hr_payslip_report'
    _wrapped_report_class = HrPayslipParser
