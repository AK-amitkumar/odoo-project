# -*- coding: utf-8 -*-

from odoo import models, fields, api
class saif_extension(models.Model):
	_name	='saif.extension'

	Employee 	 = fields.Many2one('hr.employee',string="Employee")
	date = fields.Date(string='Date', required=True)
	department	 = fields.Many2one('hr.department',string="Department")
	amount = fields.Float(string='Amount')
	returned = fields.Float(string='Returned')
	net = fields.Float(string='Net')
	payment_bank = fields.Boolean(string='Payment Through Bank')
	cash_book	 = fields.Many2one('account.bank.statement',string='Cash Book')
	s_bank	 = fields.Many2one('account.journal',string='Bank')
	s_counter	 = fields.Many2one('account.account',string='Counter Account')
	description	 = fields.Char(string='Description', required=True)
	curency	 = fields.Many2one('res.curency',string='Currency', required=True)
	proj	 = fields.Many2one('project.project',string='Project', required=True)

	state = fields.Selection([
		('exp', 'Expenses'),
		('adv', 'Advance'),
		('reim', 'Reimbursement'),
		('reim_sal', 'Reimbursement Salary'),
		('arr_sal', 'Arrears Salary'),
		('arr', 'Arrears'),
		],default='exp',string ="Type")
	# lone	 =fields.Boolean(string='Loan')
	saif_tree_link = fields.One2many('saif.ext.tree','part_id')

class saif_extension_tree(models.Model):
	_name='saif.ext.tree'
	expense_date = fields.Date(string='Expense Date', required=True)
	expense_note = fields.Char(string='Expense Note', required=True)
	expense_amount = 
	# reference=fields.Char(string='Reference')
	# unit_of_measure=fields.Many2one('product.uom',string='Unit Of Measure')
	# unit_of_price=fields.Integer(string='Unit Of Price')
	# quantities=fields.Integer(string='Quantities')
	# total=fields.Integer(string='Total')
	# part_id =fields.Many2one('saif.extension')