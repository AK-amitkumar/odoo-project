from datetime import date
from odoo import models, fields, api

class ExportLogic(models.Model):
	_name = 'export.logic'
	_rec_name = 'sr_no'

	customer         = fields.Many2one('res.partner',string="Customer",required=True)
	by_customer      = fields.Many2one('by.customer', string="By Customer",requried=True)
	sr_no       	 = fields.Char(string="SR No", readonly=True)
	bill_bol         = fields.Boolean(string="B/L")
	cont_bol         = fields.Boolean(string="Cont")
	contain          = fields.Boolean(string="Contain")
	bill_types       = fields.Char(string="Billing Type")
	our_job_no       = fields.Char(string="Our Job No", readonly=True,)
	customer_ref     = fields.Char(string="Customer Ref")
	cust_ref_inv     = fields.Char(string="Customer Ref Inv No")
	shipper_date     = fields.Date(string="DOC Received Date",default=date.today())
	mani_date        = fields.Date(string="Manifest Received Date")
	date             = fields.Date(string="Date",required=True,default=date.today())
	bill_no          = fields.Char(string="B/L Number")
	rot_no           = fields.Char(string="Rotation Number/Sequence Number")
	bill_attach      = fields.Binary(string=" ")
	eta              = fields.Date(string="ETA")
	etd              = fields.Date(string="ETD")
	about            = fields.Char(string="On Or About")
	twen_ft          = fields.Integer(string="20 ft")
	fort_ft          = fields.Integer(string="40 ft")
	bayan_no         = fields.Char(string="Bayan No")
	bayan_attach     = fields.Binary(string=" ")
	final_bayan      = fields.Char(string="Final Bayan")
	final_attach     = fields.Binary(string="Final Bayan")
	pre_bayan        = fields.Date(string="Pre Bayan Date")
	custom_exam      = fields.Boolean(string="Open Custom Examination")
	bayan_date       = fields.Date(string="Initial Bayan Date")
	shutl_start_date = fields.Date(string="Shuttling Start Date")
	fin_bayan_date   = fields.Date(string="Final Bayan Date")
	shutl_end_date   = fields.Date(string="Shuttling End Date")
	acc_link         = fields.Many2one('account.invoice',string="Invoice",readonly=True)
	status           = fields.Many2one('import.status',string="Status")
	fri_id           = fields.Many2one('freight.forward', string="Freight Link")
	site             = fields.Many2one('import.site',string="Site", required=True)
	remarks          = fields.Text(string="Remarks")
	vessel_date 	 = fields.Date(string="Vessel Arrival Date")
	vessel_name      = fields.Char(string="Vessel Name")
	s_supplier       = fields.Many2one('res.partner',string="Shipping Line")
	export_link 	 = fields.One2many('logistic.export.tree','export_tree')
	export_id 	     = fields.One2many('export.tree','crt_tree')
	export_serv 	 = fields.One2many('logistic.service.tree','service_tree')
	cont_serv 	     = fields.One2many('logistic.contain.tree','service_tree_cont')
	tick  = fields.Boolean()
	state 			 = fields.Selection([
		('draft', 'Draft'),
		('pre', 'Pre Bayan'),
		('initial', 'Initial Bayan'),
		('final', 'Final Bayan'),
		('custom_exam', 'Custom Examination'),
		('done', 'Done'),
	],default='draft')
	_sql_constraints = [
		('customer_ref', 'unique(customer_ref)','This customer reference already exists!')
	]

	@api.onchange('custom_exam')
	def change_state(self):
		"""This function change the state of Status Bar to Custom Examination"""
		if self.custom_exam:
			self.state='custom_exam'


	@api.onchange('bill_types')
	def get_tree(self):
		"""Switch Tree According to billing type"""
		if self.bill_types == "B/L Number":
			self.bill_bol = True
			self.cont_bol = False

		if self.bill_types == "Container Wise":
			self.cont_bol = True
			self.bill_bol = False


	@api.onchange('customer','by_customer')
	def get_tree_value(self):
		"""Get Billing Type of Selected customer, get data in Custom Chargers Tree according to customer and by_Customer"""
		if self.customer:
			self.bill_types = self.customer.bill_type
			if self.bill_types == "B/L Number":
				for x in self.customer.bl_id:
					if self.by_customer == x.by_customer:
						# / Delete Previous Records in Custom Charges Tree/
						delete = []
						delete = delete.append(2)
						self.export_serv = delete

						inv = []
						for invo in x:
							inv.append({
								'sevr_charge':invo.charges_serv,
								'sevr_type':invo.charges_type.id,
								'service_tree':self.id,
							})

						self.export_serv = inv

			if self.bill_types == "Container Wise":
				for x in self.customer.cont_id:
					if self.by_customer == x.by_customer:
						delete = []
						delete = delete.append(2)
						self.cont_serv = delete
						# / Delete Previous Records in Custom Charges Tree/

						inv = []
						for invo in x:
							inv.append({
								'sevr_charge_cont':invo.charges_serv,
								'sevr_type_cont':invo.charges_type.id,
								'type_contt':invo.cont_type,
								'cont_serv':self.id,
							})

						self.cont_serv = inv

	@api.model
	def create(self, vals):
		"""SR No Sequence"""
		vals['sr_no'] = self.env['ir.sequence'].next_by_code('export.logics')
		vals['our_job_no'] = self.env['ir.sequence'].next_by_code('export.job.num')
		new_record = super(ExportLogic, self).create(vals)

		return new_record
	# /(prebay, initialbay, finalbay, and over) Change the status bar /

	@api.multi
	def prebay(self):
		self.state = "pre"

	@api.multi
	def initialbay(self):
		self.state = "initial"

	@api.multi
	def finalbay(self):
		self.state = "final"

	@api.multi
	def over(self):
		self.state = "done"

	@api.multi
	def create_sale(self):
		"""Create Transport Order"""
		# / Delete the Transport Order if exist/
		prev_rec = self.env['sale.order'].search([('sales_id','=',self.id)])
		if prev_rec:
			prev_rec.unlink()

		# / Get Product having name is Container/
		get_id = self.env['product.template'].search([])
		value = 0
		for x in get_id:
			if x.name == "Container":
				value = x.id
		# / Create Transport Order/
		for data in self.export_id:
			records = self.env['sale.order'].create({
				'partner_id':self.customer.id,
				'by_customer':self.by_customer.id,
				'date_order':self.date,
				'bill_type':self.bill_types,
				'bill_no':self.bill_no,
				'suppl_name':data.transporter.id,
				'suppl_freight':data.trans_charge,
				'form':data.form.name,
				'to':data.to.name,
				'sales_id': self.id,
			})

			records.order_line.create({
				'product_id':value,
				'name':'Container',
				'product_uom_qty':1.0,
				'price_unit':data.custm_charge,
				'crt_no':data.crt_no,
				'product_uom':1,
				'order_id':records.id,
			})


	@api.multi
	def booker(self):
		# / Creating Booker List/
		lisst = []
		for x in self.export_link:
			if x.broker not in lisst:
				lisst.append(x.broker)

		invoice = self.env['account.invoice'].search([])
		invoice_lines = self.env['account.invoice.line'].search([])
		# / Creating the vendors bills/
		for line in lisst:
			create_invoice = invoice.create({
				'journal_id': 3,
				'partner_id':line.id,
				'customer':self.customer.id,
				'date_invoice' : self.date,
				'type':"in_invoice",
			})

			for x in self.export_link:
				if x.broker.name == line.name:
					create_invoice_lines= invoice_lines.create({
						'product_id':1,
						'quantity':1,
						'price_unit':x.amt_paid,
						'account_id': 3,
						'name' :'Broker Amount',
						'crt_no':x.container_no,
						'invoice_id' : create_invoice.id
					})


	@api.multi
	def create_custom_charges(self):
		""" Creating the invoice as per billing type B/L or Container wise"""
		invoice = self.env['account.invoice'].search([])
		invoice_lines = self.env['account.invoice.line'].search([])
		# / B/L Wise invoice/
		if self.bill_types == "B/L Number":

			create_invoice = invoice.create({
				'journal_id': 3,
				'partner_id':self.customer.id,
				'by_customer':self.by_customer.id,
				'date_invoice': self.date,
				'billng_type':self.bill_types,
				'bill_num':self.bill_no,
			})

			self.acc_link = create_invoice.id

			for x in self.export_serv:
				create_invoice_lines= invoice_lines.create({
					'quantity':1,
					'price_unit':x.sevr_charge,
					'account_id': 3,
					'name' :x.sevr_type.name,
					'invoice_id' : create_invoice.id
				})
		# / B/L Wise invoice/
		if self.bill_types == "Container Wise":
			data = []
			for x in self.export_id:
				if x.types not in data:
					data.append(x.types)

			create_invoice = invoice.create({
				'journal_id': 3,
				'partner_id':self.customer.id,
				'by_customer':self.by_customer.id,
				'date_invoice': self.date,
				'billng_type':self.bill_types,
				'bill_num':self.bill_no,
			})

			self.acc_link = create_invoice.id

			for line in data:
				value = 0
				for x in self.export_id:
					if x.types == line:
						value = value + 1
				get_unit = 0
				get_type = ' '
				for y in self.cont_serv:
					if y.type_contt == line:
						get_unit = y.sevr_charge_cont
						get_type = y.sevr_type_cont.name

				create_invoice_lines= invoice_lines.create({
					'quantity':value,
					'price_unit':get_unit,
					'account_id': 3,
					'name' :line,
					'service_type':get_type,
					'invoice_id' : create_invoice.id
				})



class logistics_export_tree(models.Model):
	_name = 'logistic.export.tree'

	container_no = fields.Char(string="Container No.",required=True)
	new_seal     = fields.Char(string="New Seal No")
	broker       = fields.Many2one('res.partner',string="Broker")
	amt_paid     = fields.Float(string="Paid Amount")
	export_tree = fields.Many2one('export.logic')

class service_export_tree(models.Model):
	_name = 'logistic.service.tree'

	sevr_type       = fields.Many2one('serv.types',string="Service Type")
	sevr_charge     = fields.Integer(string="Service Charges")
	service_tree = fields.Many2one('export.logic')

class service_cont_tree(models.Model):
	_name = 'logistic.contain.tree'

	sevr_type_cont       = fields.Many2one('serv.types',string="Service Type")
	sevr_charge_cont     = fields.Integer(string="Service Charges")
	type_contt           = fields.Char(string="Container Size")
	service_tree_cont    = fields.Many2one('export.logic')

class export_tree(models.Model):
	_name = 'export.tree'

	crt_no           = fields.Char(string="Container No.")
	des = fields.Char(string="Description", required=False, )
	form             = fields.Many2one('from.qoute',string="From")
	to               = fields.Many2one('to.quote',string="To")
	fleet_type       = fields.Many2one('fleet',string="Fleet Type")
	transporter      = fields.Many2one('res.partner',string="Transporter")
	trans_charge     = fields.Char(string="Transporter Charges")
	custm_charge     = fields.Char(string="Customer Charges")
	types            = fields.Selection([
		('20 ft', '20 ft'),
		('40 ft', '40 ft')],string="Size")

	crt_tree     = fields.Many2one('export.logic')

	@api.onchange('transporter','form','to','fleet_type')
	def add_charges(self):
		""" Calculating Charges As per Transporter, To, From, and fleet_type for selected customer"""

		if self.transporter.id and self.form.id and self.to.id and self.fleet_type:
			trans = self.env['res.partner'].search([('id','=',self.transporter.id)])
			for x in trans.route_id:
				if self.form.id == x.form.id and self.to.id == x.to.id and self.fleet_type == x.fleet_type and x.service_type == "export":
					self.trans_charge = x.trans_charges
			rec = self.env['res.partner'].search([('id','=',self.crt_tree.customer.id)])
			for x in rec.route_id:
				if self.form.id == x.form.id and self.to.id == x.to.id and self.fleet_type == x.fleet_type and x.service_type == "export":
					self.custm_charge = x.trans_charges

# ===========================================Import-Start===============================
# ===========================================Import-Start===============================

class ImportLogic(models.Model):
	_name = 'import.logic'
	_rec_name = 's_no'

	customer         = fields.Many2one('res.partner',string="Customer",required=True)
	by_customer      = fields.Many2one('by.customer', string="By Customer")
	bill_types       = fields.Char(string="Billing Type")
	bill_bol         = fields.Boolean(string="B/L")
	contt_bol        = fields.Boolean(string="B/L")
	contain          = fields.Boolean(string="Contain")
	s_no       	     = fields.Char(string="SR No", readonly=True)
	job_no           = fields.Char(string="Job No", readonly=True)
	date             = fields.Date(string="Date" ,required=True,default=date.today())
	customer_ref     = fields.Char(string="Customer Ref")
	cust_ref_inv     = fields.Char(string="Customer Ref Inv No" )
	site             = fields.Many2one('import.site',string="Site", required=True)
	fri_id           = fields.Many2one('freight.forward', string="Freight Link")
	shipper_date     = fields.Date(string="By Email DOC Received Date",default=date.today())
	org_date    	 = fields.Date(string="Original DOC Received Date")
	vessel_date      = fields.Date(string="Vessel Arrival Date")
	vessel_name      = fields.Char(string="Vessel Name")
	s_supplier       = fields.Many2one('res.partner',string="Shipping Line")
	bill_attach      = fields.Binary(string=" ")
	bill_no          = fields.Char(string="BL / AWB Number")
	rot_no           = fields.Char(string="Rotation Number/Sequence Number")
	twen_ft          = fields.Integer(string="20 ft")
	fort_ft          = fields.Integer(string="40 ft")
	do_attach        = fields.Binary(string=" ")
	do_no            = fields.Date(string="Do No.")
	acc_link         = fields.Many2one('account.invoice',string="Invoice",readonly=True)
	bayan_attach     = fields.Binary(string=" ")
	final_bayan      = fields.Char(string="Final Bayan")
	final_attach     = fields.Binary(string="Final Bayan")
	bayan_no         = fields.Char(string="Bayan No.")
	bayan_date       = fields.Date(string="Bayan Date")
	fin_bayan_date   = fields.Date(string="Final Bayan Date")
	status           = fields.Many2one('import.status',string="Status")
	import_id 	     = fields.One2many('import.tree','crt_tree')
	import_serv 	 = fields.One2many('import.service.tree','import_tree')
	imp_contt 	     = fields.One2many('import.contain.tree','imp_tree_cont')
	remarks          = fields.Text(string="Remarks")
	eta              = fields.Date(string="ETA")
	etd              = fields.Date(string="ETD")
	inspect_Date = fields.Date(string="Inspection Date", required=False, )
	duty_Date = fields.Date(string="Duty Paid Date", required=False, )
	gate_Date = fields.Date(string="Gate Pass Date", required=False, )
	des_Port  =  fields.Many2one(comodel_name="res.country", string="Discharging Port", required=False, )
	lan_Port  =  fields.Many2one(comodel_name="res.country", string="Landing Port", required=False, )
	tasdeer = fields.Boolean(string="Tasdeer",  )
	BRZ_In = fields.Date(string="BRZ In Date", required=False, )
	BRZ_Out = fields.Date(string="BRZ Out Date", required=False, )
	SDO_Date = fields.Date(string="SDO Collection Date", required=False, )
	ship_Type = fields.Selection(string="Shipment Type", selection=[('lcl', 'LCL'), ('fcl', 'FCL'), ], required=False, )

	tick  = fields.Boolean()
	stages 			 = fields.Selection([
		('draft', 'Draft'),
		('pre', 'Pre Bayan'),
		('initial', 'Initial Bayan'),
		('final', 'Final Bayan'),
		('done', 'Done'),
	],default='draft')

	_sql_constraints = [
		('customer_ref', 'unique(customer_ref)','This customer reference already esixts!')
	]

	@api.model
	def create(self, vals):
		"""Creating Sequence for SR No and Job No"""
		vals['s_no'] = self.env['ir.sequence'].next_by_code('import.logics')
		vals['job_no'] = self.env['ir.sequence'].next_by_code('import.job.num')
		new_record = super(ImportLogic, self).create(vals)

		return new_record


	@api.onchange('bill_types')
	def get_tree(self):
		"""Switch Tree According to billing type"""
		if self.bill_types == "B/L Number":
			self.bill_bol = True
			self.contt_bol = False

		if self.bill_types == "Container Wise":
			self.contt_bol = True
			self.bill_bol = False

	@api.onchange('customer','by_customer')
	def get_import_tree_value(self):
		if self.customer:
			self.bill_types = self.customer.bill_type
			if self.bill_types == "B/L Number":
				records = self.env['res.partner'].search([('id','=',self.customer.id)])
				for x in records.bl_id:
					if self.by_customer == x.by_customer:
						delete = []
						delete = delete.append(2)
						self.import_serv = delete

						inv = []
						for invo in x:
							inv.append({
								'charge_serv':invo.charges_serv,
								'type_serv':invo.charges_type.id,
								'import_tree':self.id,
							})

						self.import_serv = inv

			if self.bill_types == "Container Wise":
				records = self.env['res.partner'].search([('id','=',self.customer.id)])
				for x in records.cont_id:
					if self.by_customer == x.by_customer:
						delete = []
						delete = delete.append(2)
						self.imp_contt = delete

						contt = []
						for line in x:
							contt.append({
								'sevr_charge_imp':line.charges_serv,
								'sevr_type_imp':line.charges_type.id,
								'type_contt_imp':line.cont_type,
								'imp_tree_cont':self.id,
							})

						self.imp_contt = contt

	# /(prebay, initialbay, finalbay, and over) Change the status bar /
	@api.multi
	def prebay(self):
		self.stages = "pre"

	@api.multi
	def initialbay(self):
		self.stages = "initial"

	@api.multi
	def finalbay(self):
		self.stages = "final"

	@api.multi
	def over(self):
		self.stages = "done"


	@api.multi
	def create_sale(self):
		"""Create Transport Order"""
		# / Delete the Transport Order if exist/
		prev_rec = self.env['sale.order'].search([('sales_imp_id','=',self.id)])
		if prev_rec:
			prev_rec.unlink()

		# / Get Product having name is Container/
		get_id = self.env['product.template'].search([])
		value = 0
		for x in get_id:
			if x.name == "Container":
				value = x.id

		# / Create Transport Order/
		for data in self.import_id:
			records = self.env['sale.order'].create({
				'partner_id':self.customer.id,
				'by_customer':self.by_customer.id,
				'date_order':self.date,
				'suppl_name':data.transporter.id,
				'bill_type':self.bill_types,
				'bill_no':self.bill_no,
				'suppl_freight':data.trans_charge,
				'form':data.form.name,
				'to':data.to.name,
				'sales_imp_id': self.id,
			})

			records.order_line.create({
				'product_id':value,
				'name':'Container',
				'product_uom_qty':1.0,
				'price_unit':data.custm_charge,
				'crt_no':data.crt_no,
				'product_uom':1,
				'order_id':records.id,
			})

	@api.multi
	def create_custom_charges(self):

		invoice = self.env['account.invoice'].search([])
		invoice_lines = self.env['account.invoice.line'].search([])
		# / B/L Wise invoice/
		if self.bill_types == "B/L Number":

			create_invoice = invoice.create({
				'journal_id': 3,
				'partner_id':self.customer.id,
				'by_customer':self.by_customer.id,
				'date_invoice': self.date,
				'billng_type':self.bill_types,
				'bill_num':self.bill_no,
			})

			self.acc_link = create_invoice.id

			for x in self.import_serv:
				create_invoice_lines= invoice_lines.create({
					'quantity':1,
					'price_unit':x.charge_serv,
					'account_id': 3,
					'name' :x.type_serv.name,
					'invoice_id' : create_invoice.id
				})
		# / B/L Wise invoice/
		if self.bill_types == "Container Wise":
			entry = []
			for x in self.import_id:
				if x.types not in entry:
					entry.append(x.types)

			create_invoice = invoice.create({
				'journal_id': 3,
				'partner_id':self.customer.id,
				'by_customer':self.by_customer.id,
				'date_invoice': self.date,
				'billng_type':self.bill_types,
				'bill_num':self.bill_no,
			})

			self.acc_link = create_invoice.id
			for line in entry:
				value = 0
				for x in self.import_id:
					if x.types == line:
						value = value + 1
				get_unit = 0
				get_type = ' '
				for y in self.imp_contt:
					if y.type_contt_imp == line:
						get_unit = y.sevr_charge_imp
						get_type = y.sevr_type_imp.name

				create_invoice_lines= invoice_lines.create({
					'quantity':value,
					'price_unit':get_unit,
					'account_id': 3,
					'name' :line,
					'service_type':get_type,
					'invoice_id' : create_invoice.id
				})

class ImportTree(models.Model):
	_name = 'import.tree'

	crt_no       	= fields.Char(string="Container No.")
	des = fields.Char(string="Description", required=False, )
	form         	= fields.Many2one('from.qoute',string="From")
	to           	= fields.Many2one('to.quote',string="To")
	fleet_type   	= fields.Many2one('fleet',string="Fleet Type")
	# sev_typ_charg	= fields.Many2one('imp.type.tree',string="Service Type & Charges")
	transporter  	= fields.Many2one('res.partner',string="Transporter")
	trans_charge 	= fields.Char(string="Transporter Charges")
	custm_charge    = fields.Char(string="Customer Charges")
	crt_tree     = fields.Many2one('import.logic')
	types        	= fields.Selection([
		('20 ft', '20 ft'),
		('40 ft', '40 ft')],string="Size")


	@api.onchange('transporter','form','to','fleet_type')
	def add_charges(self):
		""" Calculating Charges As per Transporter, To, From, and fleet_type for selected customer"""
		if self.transporter.id and self.form.id and self.to.id and self.fleet_type:
			trans = self.env['res.partner'].search([('id','=',self.transporter.id)])
			for x in trans.route_id:
				if self.form.id == x.form.id and self.to.id == x.to.id and self.fleet_type == x.fleet_type and x.service_type == "import":
					self.trans_charge = x.trans_charges
			rec = self.env['res.partner'].search([('id','=',self.crt_tree.customer.id)])
			for x in rec.route_id:
				if self.form.id == x.form.id and self.to.id == x.to.id and self.fleet_type == x.fleet_type and x.service_type == "import":
					self.custm_charge = x.trans_charges


class ServiceImportTree(models.Model):
	_name = 'import.service.tree'

	type_serv      = fields.Many2one('serv.types',string="Service Type")
	charge_serv    = fields.Integer(string="Service Charges")
	import_tree     = fields.Many2one('import.logic')


class ImportContTree(models.Model):
	_name = 'import.contain.tree'

	sevr_type_imp       = fields.Many2one('serv.types',string="Service Type")
	sevr_charge_imp     = fields.Integer(string="Service Charges")
	type_contt_imp      = fields.Char(string="Container Size")
	imp_tree_cont       = fields.Many2one('import.logic')

class SiteLogic(models.Model):
	_name = 'import.site'
	_rec_name = 'site_name'

	site_name = fields.Char(string="Site Name")
	city      = fields.Char(string="City")
	address   = fields.Char(string="Address")
	cnt_num   = fields.Char(string="Contact No")

class StatusLogic(models.Model):
	_name = 'import.status'
	_rec_name = 'comment'
	comment = fields.Char(string="status")
