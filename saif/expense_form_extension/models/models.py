# -*- coding: utf-8 -*-

from odoo import models, fields, api
class saif_extension(models.Model):
	_name	='saif.extension'
	_rec_name = 'employee'

	employee 	 = fields.Many2one('hr.employee',string="Employee")
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
	e_currency	 = fields.Many2one('res.currency',string='Currency', required=True)
	proj	 = fields.Many2one('project.project',string='Project', required=True)
	saif_tree_link = fields.One2many('saif.ext.tree','part_id')


	state = fields.Selection([
		('exp', 'Expenses'),
		('adv', 'Advance'),
		('reim', 'Reimbursement'),
		('reim_sal', 'Reimbursement Salary'),
		('arr_sal', 'Arrears Salary'),
		('arr', 'Arrears'),
		],default='exp',string ="Type")

	status = fields.Selection([
		('draft', 'Draft'),
		('val', 'Validate'),
		],default='draft')

	@api.multi
	def val(self):
		self.status = "val"

		head = self.env['account.bank.statement'].search([('journal_id.type','=',self.cash_book.journal_id.type)])
		line = self.env['account.bank.statement.line'].search([('name','=',self.description),('amount','=',self.amount)])
		print "1111111111111111111111111111111111111111"
		print head.name
		print line
		print "1111111111111111111111111111111111111111"

		# for x in self.saif_tree_link:
		# 	if self.cash_book :
		# 		head_list.append(x.vendor)
		# for y in head_list:
		# 	create_purchase = head.create({
		# 			'partner_id':y.id,
		# 			'date_order':self.pr_date,
		# 			'date_planned':self.pr_date,
		# 			})
		# 	for x in self.saif_tree_link:
		# 		if y == x.vendor:
		# 			create_line = line.create({
		# 				'product_id':x.t_p.id,
		# 				'name': x.material_name.name,
		# 				'date_planned':self.pr_date,
		# 				'product_qty':x.qty_order,
		# 				'price_unit':x.rate,
		# 				'product_uom':x.uom.id,
		# 				'uom':x.uom.id,
		# 				'order_id':create_purchase.id,
		# 				})

	@api.multi
	def cancel(self):
		self.status = "draft"

	@api.onchange('saif_tree_link')
	def on_change_amount(self):
		if self.saif_tree_link:
			self.amount = 0.0
			for x in self.saif_tree_link:
				self.amount = self.amount + x.expense_amount


class saif_extension_tree(models.Model):
	_name='saif.ext.tree'
	expense_date = fields.Date(string='Expense Date', required=True)
	expense_note = fields.Char(string='Expense Note', required=True)
	expense_amount = fields.Float("Total Amount")
	part_id = fields.Many2one('saif.extension')