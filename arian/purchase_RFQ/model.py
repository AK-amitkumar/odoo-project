# -*- coding: utf-8 -*- 
from odoo import models, fields, api
import datetime
from datetime import datetime,date,timedelta,time
from openerp.osv import osv
from openerp.exceptions import Warning
from openerp.exceptions import ValidationError

class product_order_extension(models.Model): 
	_inherit = 'purchase.order'

	scheduled_date 		= fields.Date(string="Scheduled Date",default=datetime.today())
	departure_date 		= fields.Date(string="Departure Date",default=datetime.today())
	contact			 	= fields.Char(string="Contact No.")
	adress 				= fields.Char(string="Adress")
	incoterm 			= fields.Many2one('stock.incoterms', string="Delivery Term")
	payment_term_method = fields.Many2one('account.payment.term', string="Payment Term")
	# payment_term_id 	= fields.Many2one('account.payment.term', string="Payment Term")
	ETA 				= fields.Date(string="ETA")
	ETD 				= fields.Date(string="ETD")
	n_weight			= fields.Float(string="Net Weight")
	g_weight			= fields.Float(string="Gross Weight")
	CBM 				= fields.Float(string="CBM")
	lc_costing_link 	= fields.One2many('lc.costing','lc_costing_tab')
	shipping_doc_link 	= fields.One2many('shipping.document.attachment','shipping_doc_tree')
	# purchase_product_wizard = fields.Boolean(string="")

	transporter 		= fields.Many2one('res.partner', string="Transporter")
	forwarder 			= fields.Many2one('res.partner', string="Forwarder")
	clearing_agent 		= fields.Many2one('res.partner', string="Clearing Agent")

	ship_line 			= fields.Many2one('shipping.line')


##################### Shipping Details ########################### 
	invoice_address = fields.Char(string="Invoice Address")
	port = fields.Char(string="POD")
	loading_port = fields.Char(string="POL")
	bl_no = fields.Char(string="B/L No.")
	vessel = fields.Char(string="Vessel")
	container = fields.Char(string="Coantainer #")
	ship_mark = fields.Char(string="Ship. Mark")
	performa = fields.Char(string="performa #")
	sro = fields.Char(string="SRO #")
	s_tax_serial = fields.Char(string="GD No.")
	cnic = fields.Char(string="CNIC no")
	ntn = fields.Char(string="NTN Number")
	style = fields.Char(string="Style")
	Color = fields.Char(string="Color")
	qty_ctn = fields.Char(string="Qty/CTN")
	lot = fields.Char(string="Lot")
	pin = fields.Char(string="Pin")
	partial_shipment = fields.Char(string="Partial Shipment")
	transhipment = fields.Char(string="transhipment")
	e_form_no = fields.Char(string="E Form No")

	# ship_to_address = fields.Text(string="Ship To Address")
	# bill_to_address = fields.Text(string="Bill To Address")
	# notify = fields.Text(string="Notify")
	# other_notify = fields.Text(string="Other Notify")

	gross_weight = fields.Float(string="Gross Weight")
	net_weight = fields.Float(string="Net Weight")
	incoterm_price = fields.Float(string="Inco Term Price")

	etd_khi = fields.Date(string="ETD")
	eta = fields.Date(string="ETA")    
	bl_date = fields.Date(string="B/L Date")
	form_e_date = fields.Date(string="Form E Date")
	delivery_date = fields.Date(string="Delivery Date")
	confirmation_date = fields.Date(string="Confirmation Date")

	invoice_bank = fields.Many2one('res.bank',string="Bank")
	bank_account = fields.Many2one('res.bank',string="Bank")
	employee_name = fields.Many2one('hr.employee',string="Employee Name")
	# inco_terms = fields.Many2one('stock.incoterms',string="Inco Terms")

	state = fields.Selection([
		('draft', 'RFQ'),
		('sent', 'RFQ Sent'),
		('to approve', 'To Approve'),
		('purchase', 'Purchase Order'),
		('done', 'Locked'),
		('cancel', 'Cancelled'),
		('partial', 'Partial'),
		('complete', 'Complete'),
		],string="Custom Stages", default="draft")

	ship_via = fields.Selection([
		('bysea', 'By Sea'),
		('byair', 'By Air'),
		('byland', 'By Land'),
		],default='bysea', string="Ship via")
	ship_mode = fields.Selection([
		('bysea', 'By Sea'),
		('byair', 'By Air'),
		('byland', 'By Land'),
		],default='bysea', string="Ship Mode")

  
#--------------------------------More Detailes Variables----------------------------------------------

	company 			= fields.Char("Company")
	payments_terms 		=fields.Char("Payments Terms")
	shipment 			= fields.Char("Shipment of")
	remarks 			= fields.Char("Remarks")
	narration_1 		= fields.Text("Narration for LC (I)")
	narration_2 		= fields.Text("Narration for LC (II)")
	through_1 			= fields.Text("Through")
	applicant 			= fields.Text("Applicant")
	rebate_percentage 	= fields.Text("Rebate Percentage")
	more_info 			= fields.Text("More Info")
	under_claim 		= fields.Char("Under Claim For Rebate")
	airline 			= fields.Char("Airline")
	through_2			= fields.Char("Through")
	des 				= fields.Char("Description")
	carton_size 		= fields.Char("Carton Size")
	frieght 			=fields.Char("Frieght")
	hawb_no 			= fields.Char("H.A.W.B No")
	LC_no 				= fields.Char("LC No")
	Lc_amt 				= fields.Float("LC Amt")
	Lc_date 			= fields.Date("LC Date")
	HS_code 			= fields.Char("HS Code")
	manual_serial_no 	= fields.Char("Manual Serial #")
	manual_date 		= fields.Date("Manual Date")

	amount_total_footer = fields.Float(string="Total",readonly=True)
	per_dollar_cost 	= fields.Float(string="Per Dollar Cost",readonly=True)


	other_expense_link 	= fields.One2many('other.expense','other_expense_tree')

#-----------------------------------------


	awb_no=fields.Char("AWB No.")
	awb_date=fields.Date("AWB Date")


	@api.multi
	def complete_order(self):
		self.state = "complete"
		back_order = self.env['stock.picking'].search([('origin','=',self.name),('state','not in',('done','cancel'))])
		if back_order:
			back_order.state = "cancel"



	@api.multi
	def submitt_expense(self):
		for x in self.other_expense_link:
			journal_entries = self.env['account.move'].search([('promo_id','=',x.id)])
			journal_entries_lines = self.env['account.move.line'].search([])
			if not journal_entries:
				create_journal_entry = journal_entries.create({
					'journal_id': x.bank_type.id,
					'date':x.expense_date,
					'promo_id':x.id,
					# 'ref':"Testing",
					})
				create_debit = journal_entries_lines.create({
					'account_id':1,
					'partner_id':self.partner_id.id,
					'name':self.partner_id.name,
					'debit':x.amount,
					'move_id':create_journal_entry.id
					})
				create_credit = journal_entries_lines.create({
					'account_id':3,
					'partner_id':self.partner_id.id,
					'name':self.partner_id.name,
					'credit':x.amount,
					'move_id':create_journal_entry.id
					})
			else:
				for y in journal_entries.line_ids:
					if y.debit ==0:
						y.credit=x.amount

					if y.credit ==0:
						y.debit=x.amount

	@api.onchange('partner_id')
	def get_partner_details(self):
		if self.partner_id:
			self.contact 		= self.partner_id.phone
			self.adress 		= self.partner_id.street
			self.incoterm 		= self.partner_id.incoterm
			self.payment_term_method = self.partner_id.payment_term

	@api.onchange('lc_costing_link','other_expense_link')
	def lc_costing_total(self):
		total 			= 0
		total_dollar 	= 0

		for x in self.lc_costing_link:
			total = total + x.total_amount
			total_dollar = total_dollar + x.amount
		for y in self.other_expense_link:
			total = total + y.amount
		self.amount_total_footer = total
		if total > 0  and total_dollar > 0:
			self.per_dollar_cost = (total/total_dollar)

	@api.onchange('order_line','per_dollar_cost')
	def get_per_unit_cost(self):
		for x in self.order_line:
			x.pkr_unit_cost = self.per_dollar_cost * x.price_unit


	@api.onchange('order_line')
	def get_shippment_weight(self):
		nw_fn = 0
		gw_fn = 0
		cbm_fn = 0
		for x in self.order_line:
			nw_fn = nw_fn + (x.product_id.net_weight * x.carton)
			gw_fn = gw_fn + (x.product_id.gross_weight * x.carton)
			cbm_fn = cbm_fn + (x.product_id.cbm * x.carton)

		self.n_weight = nw_fn
		self.g_weight = gw_fn
		self.CBM = cbm_fn


	@api.multi
	def generate_wizard(self):
	  return {
	  'type': 'ir.actions.act_window',
	  'name': 'Add Products',
	  'res_model': 'wizard.class',
	  'view_type': 'form',
	  'view_mode': 'form',
	  'target' : 'new',
	  }

class product_order_line_extension(models.Model): 
	_inherit = 'purchase.order.line'

	carton 			= fields.Float(string="CARTONS")
	last_purchase 	= fields.Float(string="Last Purchase")
	pkr_unit_cost 	= fields.Float(string="Per Unit Cost(PKR)")
	qty_hand 		= fields.Float(string="Qty on Hand")
	avg_unit_price 	= fields.Float(string="Avg Price")


	@api.onchange('product_id','product_qty','carton','price_unit','pkr_unit_cost')
	def get_values(self):
		stock_history = self.env['stock.history'].search([])
		qty_on_hand = 0
		value = 0
		avg = 0
		if self.product_id:
			for x in stock_history:
				if self.product_id == x.product_id:
					if self.order_id.date_order >= x.date:
						qty_on_hand = qty_on_hand + x.quantity
						value = value + x.inventory_value
			print "xXXxxxXXXXxxXXXXXxxxXXxxxXXxxxx"
			print qty_on_hand
			print value
			self.qty_hand = qty_on_hand
			if self.qty_hand:
				avg = (value + (self.product_qty * self.price_unit))/ (qty_on_hand + self.product_qty)
			self.avg_unit_price = avg
			
		if self.product_id:
			self.pkr_unit_cost = self.order_id.per_dollar_cost * self.price_unit


	@api.onchange('product_id')
	def get_last_purchase(self):
		if self.product_id and self.order_id.partner_id:
			vendor_bill = self.env['account.invoice'].search([('type','=',"in_invoice")])
			for x in vendor_bill:
				if self.order_id.partner_id == x.partner_id:	
					for y  in x.invoice_line_ids:
						if self.product_id == y.product_id:
							self.last_sale = y.price_unit
							return


	@api.onchange('product_qty')
	def get_cartons(self):
		if self.product_qty and self.product_id:
			self.carton = self.product_qty / self.product_id.pcs_per_carton


	@api.onchange('carton')
	def get_quantity(self):
		if self.carton and self.product_id:
			self.product_qty = self.carton * self.product_id.pcs_per_carton

class shipping_document_attachment(models.Model):
	_name = 'shipping.document.attachment'

	doc_desc 			= fields.Char(string="Document Description")

	# doc_attachment 		= fields.Char(string="Attachment")
	doc_attachment 		= fields.Binary(string="Attachment")
	# doc_attachment 		= fields.many2many('ir.attachment', string="Attachments")
	shipping_doc_tree 	= fields.Many2one('purchase.order')




class lc_costing(models.Model):
	_name = 'lc.costing'

	date 				= fields.Date(string="Date", default=datetime.today())
	money_changer 		= fields.Many2one('money.changer',string="Money Changer")
	tt 					= fields.Many2one('tt.lc.costing',string="TT")
	amount				= fields.Float(string="Amount")
	conversion_rate 	= fields.Float(string="Conversion Rate")
	bank_charges 		= fields.Float(string="Bank Charges")
	with_holding_tax 	= fields.Float(string="Withholding Amount")
	total_amount 		= fields.Float(string="Total Amount") 
	lc_costing_tab 		= fields.Many2one('purchase.order')


	@api.onchange('tt')
	def count_total_tt_expense(self):
		if self.tt:
			self.amount 			= self.tt.amount
			self.conversion_rate 	= self.tt.conversion_rate
			self.bank_charges 		= self.tt.bank_charges
			self.with_holding_tax 	= self.tt.with_holding_tax
			self.total_amount 		= self.tt.total_amount

class tt_lc_costing(models.Model):
	_name = 'tt.lc.costing'

	# journal 			= fields.Many2one('account.journal', string="Bank")
	# cheque_no 			= fields.Char(string="Cheque No.")
	amount				= fields.Float(string="Amount")
	amount_pkr 			= fields.Float(string="Amount Paid (PKR)", default=0)
	conversion_rate 	= fields.Float(string="Conversion Rate")
	bank_charges 		= fields.Float(string="Bank Charges")
	with_holding_tax 	= fields.Float(string="Withholding Amount")
	total_amount 		= fields.Float(string="Total Amount To be Paid (PKR)" , default=0) 
	# haulage_expense 	= fields.Float(string="Haulage & Other Expense") 
	name 				= fields.Many2one('purchase.order',string="PO No.")
	tt_lc_costing_link 	= fields.One2many('tt.lc.costing.line','tt_lc_costing_tree')




	# @api.onchange('other_expense_link')
	# def count_total_haulage_expense(self):
	# 	haulage_expense_fn	= 0

	# 	for x in self.other_expense_link:
	# 		haulage_expense_fn 	= haulage_expense_fn + x.total_amount
	# 	self.haulage_expense 	= haulage_expense_fn
	# 	self.total_amount 		= self.total_amount + haulage_expense_fn





	@api.model
	def create(self, vals):	
		new_record = super(tt_lc_costing, self).create(vals)
		if new_record.amount_pkr != new_record.total_amount:
			raise Warning('Paid Amount and Pending Amount is not Equal')
			# raise ValidationError('Paid Amount and Pending Amount is not Equal')

		return new_record

	@api.multi
	def write(self, vals):	
		super(tt_lc_costing, self).write(vals)
		if self.amount_pkr != self.total_amount:
			raise ValidationError('Paid Amount and Pending Amount is not Equal')
		return True

	@api.onchange('amount','conversion_rate','bank_charges','with_holding_tax')
	def count_total_tt_costing(self):
		if self.amount and self.conversion_rate and self.bank_charges and self.with_holding_tax:
			self.total_amount = (self.amount * self.conversion_rate) + self.bank_charges + self.with_holding_tax


	@api.onchange('tt_lc_costing_link')
	def count_total_paid_amount(self):

		total_pkr			= 0
		for x in self.tt_lc_costing_link:
			total_pkr = total_pkr + x.amount
		self.amount_pkr = total_pkr

		# 	amount_fn 			= amount_fn + x.amount
		# 	conversion_rate_fn 	= conversion_rate_fn + x.conversion_rate
		# 	bank_charges_fn 	= bank_charges_fn + x.bank_charges
		# 	wh_tax_fn 			= wh_tax_fn + x.with_holding_tax
		# 	total_amount_fn 	= total_amount_fn + x.total_amount
		

		# self.amount 			= amount_fn
		# self.conversion_rate 	= conversion_rate_fn
		# self.bank_charges 		= bank_charges_fn
		# self.with_holding_tax 	= wh_tax_fn
		# self.total_amount 		= total_amount_fn


class tt_lc_costing_form(models.Model):
	_name = 'tt.lc.costing.line'

	journal 			= fields.Many2one('account.journal', string="Bank", required=True)
	cheque_no 			= fields.Char(string="Cheque No.", required=True)
	amount				= fields.Float(string="Amount (PKR)",required=True)
	# conversion_rate 	= fields.Float(string="Conversion Rate",required=True)
	# bank_charges 		= fields.Float(string="Bank Charges",required=True)
	# with_holding_tax 	= fields.Float(string="Withholding Amount",required=True)
	# total_amount 		= fields.Float(string="Total Amount")
	name 				= fields.Many2one('purchase.order',string="PO No.")
	tt_lc_costing_tree 	= fields.Many2one('tt.lc.costing')

	# @api.onchange('amount','conversion_rate','bank_charges','with_holding_tax')
	# def count_total(self):
	# 	self.total_amount = self.amount + self.conversion_rate + self.bank_charges + self.with_holding_tax

class account_journal_extension(models.Model):
	_inherit = 'account.journal'

	with_holding_rate = fields.Float(string="Withholding Rate")


class other_expense(models.Model):
	_name = 'other.expense'


	expense_type 		= fields.Many2one('haulage.expense')
	amount 				= fields.Float(string="Amount")
	bank_type 			= fields.Many2one('account.journal')
	expense_date 		= fields.Date(string="Date", default=date.today())
	# custom_duty 			= fields.Float(string="Custom Duty",required=True)
	# sales_income_tax 		= fields.Float(string="S/Tax, IN/Tax",required=True)
	# freight 				= fields.Float(string="Freight",required=True)
	# ca_bill 				= fields.Float(string="C/A Bill",required=True)
	# labour 					= fields.Float(string="Labour",required=True)
	# wh_tax 					= fields.Float(string="W/H Tax",required=True)
	# advertisement_budget 	= fields.Float(string="Advertisement Budget",required=True)
	# dealer_incentice_budget = fields.Float(string="Dealer Incentice Budget",required=True)
	# bank_wh_tax 			= fields.Float(string="Bank W/H Tax",required=True)
	# placement_jk_land 		= fields.Float(string="Placement JK Land",required=True)
	# total_amount 			= fields.Float(string="Total Amount")
	other_expense_tree 		= fields.Many2one('purchase.order') 

	@api.multi
	def unlink(self):
		super(other_expense,self).unlink()
		pricelist = self.env['account.move'].search([('promo_id','=', self.id)])
		if pricelist:
			pricelist.unlink()

		return True


	# @api.onchange('haulage','custom_duty','sales_income_tax','freight','ca_bill','labour','wh_tax','advertisement_budget','total_amount','placement_jk_land','bank_wh_tax','dealer_incentice_budget')
	# def count_total(self):
	# 	self.total_amount = self.haulage.haulage_amount + self.custom_duty + self.sales_income_tax + self.freight + self.ca_bill + self.labour + self.wh_tax + self.advertisement_budget +self.dealer_incentice_budget + self.bank_wh_tax +self.placement_jk_land


class haulage_expense(models.Model):
	_name ='haulage.expense'

	name 	 			= fields.Char(string="Expense Name")
	haulage_journal 	= fields.Many2one('account.account')	




class money_changer(models.Model):
	_name ='money.changer'

	name 	 		= fields.Char(string="Name")
	adress 			= fields.Char(string="Adress")	
	tele_phone 		= fields.Char(string="Telephone No.")	



class shipping_line(models.Model):
	_name = 'shipping.line'

	name = fields.Char(string="Shipping Line")