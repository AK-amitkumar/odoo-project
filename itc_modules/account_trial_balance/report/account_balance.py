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

import time

from odoo import models,api
from openerp.report import report_sxw
# from openerp.addons.account.report.common_report_header import common_report_header
from openerp.exceptions import ValidationError


# class account_balance_new(report_sxw.rml_parse, common_report_header):
class account_balance_new(report_sxw.rml_parse):
    _name = 'report.account.account.balance.new'

    # def __init__(self, cr, uid, name, context=None):
    #     super(account_balance_new, self).__init__(cr, uid, name, context=context)
    #     self.sum_debit = 0.00
    #     self.sum_credit = 0.00
    #     self.date_lst = []
    #     self.date_lst_string = ''
    #     self.result_acc = []
    #     self.calculate_acc = []
    #     self.localcontext.update({
    #         'time': time,
    #         'lines': self.lines,
    #         'sum_debit': self._sum_debit,
    #         'sum_credit': self._sum_credit,
    #         'get_fiscalyear':self._get_fiscalyear,
    #         'get_filter': self._get_filter,
    #         'get_start_period': self.get_start_period,
    #         'get_end_period': self.get_end_period ,
    #         'get_account': self._get_account,
    #         'get_journal': self._get_journal,
    #         'get_start_date':self._get_start_date,
    #         'get_end_date':self._get_end_date,
    #         'get_target_move': self._get_target_move,
    #         'sum_init_debit_account':self._sum_init_debit_account,
    #         'sum_init_credit_account':self._sum_init_credit_account,
    #         'sum_balance_debit_credit':self._sum_balance_debit_credit,
    #         'get_start_level':self._get_start_level,
    #         'get_code_from':self._get_code_from,
    #         'get_code_to':self._get_code_to,
    #         'cal_total_lines':self._cal_total_lines,
    #     })
    #     self.context = context

    # def set_context(self, objects, data, ids, report_type=None):
    #     new_ids = ids
    #     if (data['model'] == 'ir.ui.menu'):
    #         new_ids = 'chart_account_id' in data['form'] and [data['form']['chart_account_id']] or []
    #         objects = self.pool.get('account.account').browse(self.cr, self.uid, new_ids)
    #     context = data['form'].get('used_context',{})
    #     obj_move = self.pool.get('account.move.line')
    #     journal_ids = self.pool.get('account.journal').search(self.cr, self.uid, [])
    #     data['form'].get('used_context',{}).update({'journal_ids':journal_ids})
    #     context['fiscalyear'] = data['form']['fiscalyear_id']
    #     if data['form']['filter'] == 'filter_period':
    #         period_obj = self.pool.get('account.period')
    #         start_period = period_obj.browse(self.cr, self.uid, context.get('period_from',False), context=context)
    #         end_period = period_obj.browse(self.cr, self.uid, context.get('period_to',False), context=context)
    #         context.update({'date_from':start_period and start_period.date_start or False,
    #                         'date_to':end_period and end_period.date_stop or False,
    #                         'period_from':False,'period_to':False})
    #     if data['form']['filter'] == 'filter_no':
    #         context.update({'no_init':True})
    #     self.sortby = data['form'].get('sortby', 'sort_date')
    #     ctx2 = context.copy()
    #     self.ctx2 = ctx2
    #     if data['form']['filter'] != 'filter_no':
    #         ctx2.update({'initial_bal':True})
    #         self.init_query = obj_move._query_get(self.cr, self.uid, obj='l', context=ctx2)
    #     self.target_move = data['form'].get('target_move', 'all')
        
    #     return super(account_balance_new, self).set_context(objects, data, new_ids, report_type=report_type)
    
    # def _get_code_from(self, account_from):
    #     code_from = ''
    #     if account_from:
    #         obj_account = self.pool.get('account.account')
    #         code_from = obj_account.browse(self.cr, self.uid, account_from[0]).code
    #     return code_from
    
    # def _get_code_to(self, account_to):
    #     code_to = ''
    #     if account_to:
    #         obj_account = self.pool.get('account.account')
    #         code_to = obj_account.browse(self.cr, self.uid, account_to[0]).code
    #     return code_to
    
    
    # def _get_start_level(self, data):
    #     return 0
    
    # def _sum_init_credit_account(self, account):
    #     account_obj = self.pool.get('account.account')
    #     context = self.ctx2
    #     if context.get('no_init',False):
    #         return 0.0
    #     account = account_obj.browse(self.cr, self.uid, account, context=context)
    #     if account.type == 'view':
    #         return account.credit
    #     move_state = ['draft','posted']
    #     if self.target_move == 'posted':
    #         move_state = ['posted','']
    #     self.cr.execute('SELECT sum(credit) \
    #             FROM account_move_line l \
    #             JOIN account_move am ON (am.id = l.move_id) \
    #             WHERE (l.account_id = %s) \
    #             AND (am.state IN %s) \
    #             AND '+ self.init_query +' '
    #             ,(account.id, tuple(move_state)))
    #     # Add initial balance to the result
    #     sum_credit = self.cr.fetchone()[0] or 0.0
    #     return sum_credit
    
    
    # def _sum_init_debit_account(self, account):
    #     account_obj = self.pool.get('account.account')
    #     context = self.ctx2
    #     if context.get('no_init',False):
    #         return 0.0
    #     account = account_obj.browse(self.cr, self.uid, account, context=context)
    #     if account.type == 'view':
    #         return account.debit
    #     move_state = ['draft','posted']
    #     if self.target_move == 'posted':
    #         move_state = ['posted','']
    #     self.cr.execute('SELECT sum(debit) \
    #             FROM account_move_line l \
    #             JOIN account_move am ON (am.id = l.move_id) \
    #             WHERE (l.account_id = %s) \
    #             AND (am.state IN %s) \
    #             AND '+ self.init_query +' '
    #             ,(account.id, tuple(move_state)))
    #     # Add initial balance to the result
    #     sum_debit = self.cr.fetchone()[0] or 0.0
    #     return sum_debit
    
    
    # def _sum_balance_debit_credit(self, account,trans_dr_amt,trans_cr_amt):
    #     debit_sum = self._sum_init_debit_account(account)
    #     debit_sum += trans_dr_amt
        
    #     credit_sum = self._sum_init_credit_account(account)
    #     credit_sum += trans_cr_amt
    #     balance = debit_sum - credit_sum
    #     if balance < 0:
    #         return {'debit':0.0, 'credit':balance*-1}
    #     return {'debit':balance, 'credit':0.0}
        

    # def _get_account(self, data):
    #     if data['model']=='account.account':
    #         return self.pool.get('account.account').browse(self.cr, self.uid, data['form']['id']).company_id.name
    #     return super(account_balance_new ,self)._get_account(data)
    
    # def _cal_total_lines(self, form, test_ids, ids=None, done=None):
        
    #     opt_test={}
    #     for test_id in test_ids:
    #         opt_test[test_id['id']] = test_id
        
    #     for opt in opt_test:
    #         flag = False
    #         for t in test_ids:
                
    #             if t['parent_id'] and t['parent_id'][0]==opt:
    #                 flag =True
    #                 break
    #         if flag:
    #             continue
    #         else:
    #             self.calculate_acc.append(opt_test[opt])
    #     o_debit = o_credit = t_debit = t_credit = b_debit = b_credit = 0.0
    #     for acc_data in self.calculate_acc:
    #         o_debit += self._sum_init_debit_account(acc_data['id'])
    #         o_credit += self._sum_init_credit_account(acc_data['id'])
            
    #         t_debit += acc_data['debit']
    #         t_credit += acc_data['credit']
            
    #         b_debit += self._sum_balance_debit_credit(acc_data['id'],acc_data['debit'],acc_data['credit'])['debit']
    #         b_credit += self._sum_balance_debit_credit(acc_data['id'],acc_data['debit'],acc_data['credit'])['credit']
    #     return [{'o_debit':o_debit, 'o_credit':o_credit, 't_debit':t_debit, 't_credit':t_credit, 'b_debit':b_debit, 'b_credit':b_credit}]
    

    # def lines(self, form, ids=None, done=None):
    #     def _process_child(accounts, disp_acc, parent):
    #             account_rec = [acct for acct in accounts if acct['id']==parent][0]
    #             currency_obj = self.pool.get('res.currency')
    #             acc_id = self.pool.get('account.account').browse(self.cr, self.uid, account_rec['id'])
    #             currency = acc_id.currency_id and acc_id.currency_id or acc_id.company_id.currency_id
    #             res = {
    #                 'id': account_rec['id'],
    #                 'type': account_rec['type'],
    #                 'code': account_rec['code'],
    #                 'name': account_rec['name'],
    #                 'level': account_rec['level'],
    #                 'debit': account_rec['debit'],
    #                 'credit': account_rec['credit'],
    #                 'balance': account_rec['balance'],
    #                 'parent_id': account_rec['parent_id'],
    #                 'bal_type': '',
    #                 'print':'yes',
    #             }
    #             self.sum_debit += account_rec['debit']
    #             self.sum_credit += account_rec['credit']
    #             if disp_acc == 'movement':
    #                 if currency_obj.is_zero(self.cr, self.uid, currency, res['credit']) and currency_obj.is_zero(self.cr, self.uid, currency, res['debit']) and currency_obj.is_zero(self.cr, self.uid, currency, res['balance']):
    #                    res.update({'print':'no'})   
    #             elif disp_acc == 'not_zero':
    #                 if currency_obj.is_zero(self.cr, self.uid, currency, res['balance']):
    #                     res.update({'print':'no'})   
    #             self.result_acc.append(res)
                
    #             if account_rec['child_id']:
    #                 for child in account_rec['child_id']:
    #                     _process_child(accounts,disp_acc,child)

    #     obj_account = self.pool.get('account.account')
    #     if not ids:
    #         ids = self.ids
    #     if not ids:
    #         return []
    #     if not done:
    #         done={}

    #     ctx = self.context.copy()
    #     ctx['fiscalyear'] = form['fiscalyear_id']
    #     if form['filter'] == 'filter_period':
    #         period_obj = self.pool.get('account.period')
    #         start_period = period_obj.browse(self.cr, self.uid, form['period_from'], context=ctx)
    #         end_period = period_obj.browse(self.cr, self.uid, form['period_to'], context=ctx)
    #         ctx.update({'date_from':start_period and start_period.date_start or False,
    #                         'date_to':end_period and end_period.date_stop or False,
    #                         'period_from':False,'period_to':False})

    #     elif form['filter'] == 'filter_date':
    #         ctx['date_from'] = form['date_from']
    #         ctx['date_to'] =  form['date_to']
    #     ctx['state'] = form['target_move']
    #     parents = ids
    #     child_ids = obj_account._get_children_and_consol(self.cr, self.uid, ids, ctx)
    #     if child_ids:
    #         ids = child_ids
    #     accounts = obj_account.read(self.cr, self.uid, ids, ['type','code','name','debit','credit','balance','parent_id','level','child_id'], ctx)

    #     for parent in parents:
    #             if parent in done:
    #                 continue
    #             done[parent] = 1
    #             _process_child(accounts,form['display_account'],parent)
    #     if form.get('filter_level',False) or form.get('filter_account',False):
    #         level_result = []
    #         if form['filter_level']:
    #             for rec_dict in self.result_acc:
    #                 if int(rec_dict['level']) >= int(form['level_from']) and int(rec_dict['level']) <= int(form['level_to']):
    #                     continue
    #                 else:rec_dict.update({'print':'no'})
    #     return self.result_acc


class report_trialbalance(models.Model):
    _name = 'report.account_trial_balance.report_trialbalance_new'
    _inherit = 'report.abstract_report'
    _template = 'account_trial_balance.report_trialbalance_new'
    _wrapped_report_class = account_balance_new

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
