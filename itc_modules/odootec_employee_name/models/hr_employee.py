# -*- coding: utf-8 -*-
# 
# OpenERP, Open Source Management Solution
# Copyright (C) 2004-2010 OdooTec (<http://odootec.com>).
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

from openerp import models, fields, api, _, SUPERUSER_ID
import openerp.addons.decimal_precision as dp


class HrResource(models.Model):
    _inherit = 'resource.resource'
    name = fields.Char('Name', required=False, translate=True)




class hr_employee(models.Model):
    _inherit = "hr.employee"

    # @api.cr_context
    # def _auto_init(self, cr, context=None):
    #     super(hr_employee, self)._auto_init(cr, context=context)
    #     self._update_employee_names(cr, SUPERUSER_ID, context=context)

    # @api.model
    # def split_name(self, name):
    #     name = u" ".join(name.split(None)) if name else name
    #     parts = name.strip().split(" ", 3)
    #     if len(parts) < 4:
    #         for i in range(0, 4-len(parts)):
    #             parts.append(False)

    #     return {"first_name": parts[0], "second_name": parts[1], "third_name": parts[2], "last_name": parts[3]}

    # @api.model
    # def _update_employee_names(self):
    #     employees = self.search([
    #         ('first_name', '=', ' ')])
    #     for ee in employees:
    #         names = self.split_name(ee.name_related)
    #         ee.write(names)

    def _firstname_default(self):
        return ' ' if self.env.context.get('module') else False

    first_name = fields.Char('First Name', translate=True, required=False, default=_firstname_default)
    second_name = fields.Char('Father Name', translate=True, required=False, default=_firstname_default)
    third_name = fields.Char('Grandfather Name', translate=True, required=False)
    last_name = fields.Char('Last Name', translate=True, required=False, default=_firstname_default)
    employee_id = fields.Char('Employee ID', required=False, readonly=False, copy=False)

    # @api.onchange('first_name', 'second_name', 'third_name', 'last_name')
    # def _onchange_name(self):
    #     self.name = self.get_original_name(self.first_name, self.second_name, self.third_name, self.last_name)

    # @api.multi
    # def get_original_name(self, first_name, second_name, third_name, last_name):
    #     name = ''
    #     if first_name:
    #         name = first_name
    #     if second_name:
    #         name += ' ' + second_name
    #     if third_name:
    #         name += ' ' + third_name
    #     if last_name:
    #         name += ' ' + last_name
    #     return name

    # @api.one
    # def write(self, vals):
    #     for record in self:
    #         vals['name'] = self.get_original_name(vals.get('first_name', record.first_name),
    #                                           vals.get('second_name', record.second_name),
    #                                           vals.get('third_name', record.third_name),
    #                                           vals.get('last_name', record.last_name))
    #         return super(hr_employee, self).write(vals)