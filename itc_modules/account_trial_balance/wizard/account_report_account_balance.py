# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
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
##############################################################################

from odoo import models, fields, api
from openerp.tools.translate import _

class account_balance_report(models.Model):
    _inherit = "account.common.account.report"
    _name = 'account.balance.report.new'
    _description = 'Trial Balance Report new'

    
    journal_ids =  fields.Many2many('account.journal', 'account_balance_report_journal_rel', 'account_id', 'journal_id', 'Journals', required=True)
    filter_level = fields.Boolean('Filter By Level')
    filter_account = fields.Boolean('Filter By Account')
    level_from = fields.Selection([('0','0'),('1','1'),('2','2'),('3','3'),('4','4'),('5','5'),('6','6'),('7','7'),('8','8'),('9','9')], string = 'Level From')
    level_to = fields.Selection([('0','0'),('1','1'),('2','2'),('3','3'),('4','4'),('5','5'),('6','6'),('7','7'),('8','8'),('9','9')], string = 'Level To')
    account_from = fields.Many2one('account.account','Account From')
    account_to = fields.Many2one('account.account','Account To')
#     
        
    

    _defaults = {
        'journal_ids': [],
        'filter_level':False,
        'filter_account':False,
    }

#     def onchange_filter_account(self,cr, uid, ids, filter_account, display_account, context=None):
#         res = {'value':{'display_account':display_account}}
# #         if filter_account:
# #             res['value'].update({'display_account': 'all'})
#         return res
    
#     def _print_report(self, cr, uid, ids, data, context=None):
#         data = self.pre_print_report(cr, uid, ids, data, context=context)
#         data['form'].update(self.read(cr, uid, ids, ['filter_level','filter_account','level_from','level_to','account_from','account_to'], context=context)[0])
# #         if data['form']['filter_account'] and data['form']['display_account'] != 'all':
# #             raise osv.except_osv(_('Warning!'),
# #                         _('For Filter By Account , please select Display Account : all.'))
             
#         context.update({'landscape':True})
#         return self.pool['report'].get_action(cr, uid, [], 'account_trial_balance.report_trialbalance_new', data=data, context=context)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
