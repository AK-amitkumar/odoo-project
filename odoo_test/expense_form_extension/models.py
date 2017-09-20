# # -*- coding: utf-8 -*-

from openerp import models, fields, api
from openerp.exceptions import ValidationError
from openerp.exceptions import Warning
from datetime import datetime as dt
from dateutil import relativedelta as rd

class expense_form_extension(models.Model):

	_inherit = 'hr.expense.expense'

	hide_button1 		= fields.Boolean()
	hide_button2 		= fields.Boolean()
	advance      		= fields.Float('Amount')
	returned     		= fields.Float()
	net          		= fields.Float(readonly = True, compute="_compute_total_line")
	cash_book    		= fields.Many2one('account.bank.statement', string = "Cash Book", domain="[('state','=','open')]")
	payment_from_bank   = fields.Boolean('Payment Through Bank')
	bank_available	    = fields.Many2one('account.journal',string='Bank', domain="[('type','=','bank')]")
	counter_account     = fields.Many2one('account.account', string="Counter Account")
	
	@api.multi
	def _compute_total_line(self):
		self.net = self.advance - self.returned

	@api.multi
	def my_btn(self):
		self.write({'state': 'paid'})

	@api.multi
	def advance_btn(self):

		self.hide_button1=True
		statement_recs =self.env['account.bank.statement'].search([('id','=',self.cash_book.id)])
		y=0
		for x in statement_recs:
			y += 1
		if y>1:
			raise Warning('Multiple Cash Books are open..Only one required')
		elif y<1:
			raise Warning('No Cash Book is open!')
		else:
			respected_tree =statement_recs.line_ids
			x=0
			for n in respected_tree:
				x=x+1
			respected_tree.create({
		    	'sequence':x+1,
		    	'statement_id': statement_recs.id,
		    	'date' :self.date,
		    	'name': self.name,
		    	'employee':self.employee_id.id,
		    	'amount':self.advance *-1
		    	})
	
	@api.multi
	def returned_btn(self):
		self.hide_button2=True
		statement_recs =self.env['account.bank.statement'].search([('state','=','open')])
		y=0
		for x in statement_recs:
			y += 1
		if y>1:
			raise Warning('Multiple Cash Books are open..Only one required')
		elif y<1:
			raise Warning('No Cash Book is open!')
		else:
			respected_tree =statement_recs.line_ids
			x=0
			for n in respected_tree:
				x=x+1
			respected_tree.create({
				'sequence':x+1,
				'statement_id': statement_recs.id,
				'date' :self.date,
				'name': self.name,
				'employee':self.employee_id.id,
				'amount':self.returned
				})

	@api.multi
	def post_btn(self):
		JournalEntry = self.env['account.move']
		JournalEntryLines = self.env['account.move.line']
		if not JournalEntry.search([('id','=',self.id)]):
			journalentry_id = JournalEntry.create({
				'journal_id': self.env['account.journal'].search([('code','=','EXJ')]).id,
				'date':self.date,
				'ecube_expense_id':self.id,
				})
			JournalEntryLines.create({
				'account_id':self.counter_account.id,
				# 'partner_id':self.partner_id.id,
				'name':self.employee_id.name,
				'move_id':journalentry_id.id,
				'debit':self.advance,
				'credit':0.0,
				})
			JournalEntryLines.create({
				'account_id':self.bank_available.default_debit_account_id.id,
				# 'partner_id':self.partner_id.id,
				'name':self.employee_id.name,
				'move_id':journalentry_id.id,
				'debit':0.0,
				'credit':self.advance,
				})
		else:
			record = JournalEntry.search([('id','=',self.id)])
			record.date = self.date
			record.line_id.unlink()

			JournalEntryLines = self.env['account.move.line']
			
			JournalEntryLines.create({
				'account_id':self.counter_account.id,
				# 'partner_id':self.partner_id.id,
				'name':self.employee_id.name,
				'move_id':record.id,
				'debit':self.advance,
				'credit':0.0,
				})
			JournalEntryLines.create({
				'account_id':self.bank_available.default_debit_account_id.id,
				# 'partner_id':self.partner_id.id,
				'name':self.employee_id.name,
				'move_id':record.id,
				'debit':0.0,
				'credit':self.advance,
				})
class expense_form_extension_1(models.Model):
	_inherit = 'account.bank.statement.line'
	employee = fields.Many2one('hr.employee')

class loan_management(models.Model):
	_inherit = 'hr.expense.expense'

	loan             = fields.Boolean()
	skip_loan        = fields.Boolean('Skip Loan')
	loan_start_date  = fields.Date('Start Date')
	loan_end_date    = fields.Date('End Date')
	installments     = fields.Integer(string="No of Installment")
	loan_paid        = fields.Float(string="Loan Paid")
	loan_remaining   = fields.Float(string="Loan Remaining")
	amount_per_month = fields.Float(string="Amount per Month")
	amount_manual    = fields.Float(string="Manual Amount")
	pringle          = fields.One2many('loan.1122','cringle')	
	types            = fields.Selection([
		('advance', 'Advance'),
        ('reimbursement', 'Reimbursement'),
        ('reimbursement_salery', 'Reimbursement Salary'),
        ('arrears_salery', 'Arrears Salary'),
        ('arrears', 'Arrears'),
        ('other', 'Other'),
        ],string='Type')

	@api.multi
	def show_btn(self):
		self.pringle.unlink()
		nn = str(self.employee_id.name)
		active_class =self.env['hr.payslip.line'].search([('employee_id','=',nn)])
		start_date_1  = dt.strptime(self.loan_start_date, "%Y-%m-%d")
		end_date_1   = dt.strptime(self.loan_end_date, "%Y-%m-%d")
		for x in active_class:
			start_date = str(x.slip_id.date_from)
			end_date = str(x.slip_id.date_to)
			start_date = dt.strptime(start_date[2:], "%y-%m-%d")
			end_date   = dt.strptime(end_date[2:], "%y-%m-%d")
			if x.code == 'SDM' and start_date >= start_date_1 and end_date_1>=end_date:
				for y in self:
					y.pringle.create({
						'name'     : x.name,
						'date'     : x.slip_id.date_from,
						'slip_id'  : x.slip_id.id,
						'amount'   : x.amount,
						'cringle'  : y.id
						})
		# ---------------------------------------------------------
		r = rd.relativedelta(end_date_1, start_date_1)
		if r.years > 0 :
			years = r.years * 12
			months = r.months +1
			self.installments = years + months
		else:
			self.installments = r.months +1
		# ---------------------------------------------------------
		if self.loan != False and self.installments != 0:
			self.amount_per_month= self.advance / self.installments
		elif self.loan != False and self.installments == 0:
			self.amount_per_month= self.advance * 0
		# ---------------------------------------------------------
		self.loan_paid = sum(line.amount for line in self.pringle)
		self.loan_remaining = self.advance - self.loan_paid
		
class loan_management_1122(models.Model):
	_name = 'loan.1122'
	name = fields.Char()
	date = fields.Date()
	slip_id = fields.Integer()
	amount = fields.Float()
	cringle  = fields.Many2one('hr.expense.expense',
        ondelete='cascade')

class hr_employee(models.Model):
    _inherit = 'hr.employee'

    @api.model
    def loan_ded(self, payslip):

    	duration = 0.0
        tsheet_obj = self.env['hr.expense.expense']
        timesheets = tsheet_obj.search([('employee_id', '=', self.id), 
            ('loan_start_date', '<=', payslip.date_from), ('loan_end_date', '>=', payslip.date_to),('loan', '=', True)])
        for tsheet in timesheets:
    		if tsheet.skip_loan == True :
    			duration = duration + 0
    		elif tsheet.amount_manual > 0 :
    			duration = duration + tsheet.amount_manual
        	else:
        		duration = duration + tsheet.amount_per_month
        return duration
    
    @api.model
    def advance_ded(self, payslip):
    	
        t_advance = 0.0
        tsheet_obj = self.env['hr.expense.expense']
        timesheets = tsheet_obj.search([('employee_id', '=', self.id), ('types', '=', 'advance'),
        	('date', '>=', payslip.date_from), ('date', '<=', payslip.date_to)])
        for tsheet in timesheets:
            t_advance = t_advance + tsheet.advance
        return t_advance

    @api.model
    def reimbursement_salary_ded(self, payslip):
    	
        t_advance = 0.0
        tsheet_obj = self.env['hr.expense.expense']
        timesheets = tsheet_obj.search([('employee_id', '=', self.id), ('types', '=', 'reimbursement_salery'),
        	('date', '>=', payslip.date_from), ('date', '<=', payslip.date_to)])
        for tsheet in timesheets:
            t_advance = t_advance +tsheet.advance
        return t_advance

    @api.model
    def arrears_salary_ded(self, payslip):
    	
        t_advance = 0.0
        tsheet_obj = self.env['hr.expense.expense']
        timesheets = tsheet_obj.search([('employee_id', '=', self.id), ('types', '=', 'arrears_salery'),
        	('date', '>=', payslip.date_from), ('date', '<=', payslip.date_to)])
        for tsheet in timesheets:
            t_advance = t_advance +tsheet.advance
        return t_advance

    @api.model
    def total_loan(self, payslip):
    	
        t_advance = 0.0
        tsheet_obj = self.env['hr.expense.expense']
        timesheets = tsheet_obj.search([('employee_id', '=', self.id), 
            ('loan_start_date', '<=', payslip.date_from), ('loan_end_date', '>=', payslip.date_to), ('loan', '=', True)])
        for tsheet in timesheets:
    		t_advance = t_advance + tsheet.advance
        return t_advance

    @api.model
    def total_loan_ded(self, payslip):
    	
    	expense_rec = self.env['hr.expense.expense'].search([('employee_id', '=', self.id), 
            ('loan_start_date', '<=', payslip.date_from), ('loan_end_date', '>=', payslip.date_to), ('loan', '=', True)])

    	start_date_1 = ''
    	end_date_1 = ''
    	amount = 0

    	for x in expense_rec:
    		if start_date_1 == '':
    			start_date_1 =  dt.strptime(x.loan_start_date, "%Y-%m-%d")
    		
    		elif start_date_1 >= dt.strptime(x.loan_start_date, "%Y-%m-%d"):
    			start_date_1 =  dt.strptime(x.loan_start_date, "%Y-%m-%d")
    		else:
    			pass

    		if end_date_1 == '':
    			end_date_1 = dt.strptime(x.loan_end_date, "%Y-%m-%d")
    		elif end_date_1 <=  dt.strptime(x.loan_end_date, "%Y-%m-%d"):
    			end_date_1 = dt.strptime(x.loan_end_date, "%Y-%m-%d")
    		else:
    			pass

    	if start_date_1 and end_date_1:
    		payslip_rec = self.env['hr.payslip'].search([('employee_id', '=', self.id),('date_from','>=',start_date_1),('date_to','<=',end_date_1)])
    		for x in payslip_rec:
    			if x.line_ids:
    				for y in x.line_ids:
    					if y.code == 'SDM' and payslip.date_from > y.slip_id.date_from:
    						amount = amount + y.amount
    		return amount
    	else:
    		return 0

class EcubeAccountMoveLineInherit(models.Model):
	_inherit = 'account.move.line'
	ecube_employee_id  = fields.Many2one('hr.employee', string="Employee")


class EcubeAccountMoveInherit(models.Model):
	_inherit = 'account.move'
	ecube_expense_id  = fields.Many2one('hr.expense.expense', string="Expense", ondelete='cascade')
