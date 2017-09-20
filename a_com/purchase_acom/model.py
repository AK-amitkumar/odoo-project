# -*- coding: utf-8 -*- 
from odoo import models, fields, api

class acom_invoice_extension(models.Model): 
	_inherit = 'account.invoice.line'

	assessed_Price = fields.Float(string = "Assessed Price")



class acom_purchase_line_extension(models.Model):

	_inherit = 'purchase.order.line'
	assessed_Price = fields.Float(string = "Assessed Price")



class acom_purchase_extension(models.Model):

	_inherit = 'purchase.order'
	# amount_tax=partner_ref

	@api.onchange('order_line')
	def onChBcubeTaxes(self):
		t_tax = 0.0
		self.amount_tax = 0.0
		for x in self.order_line:
			self.t_tax = self.calculateTaxAmount(x.taxes_id, x.product_qty, x.assessed_Price)
			self.amount_tax =self.amount_tax + self.t_tax
			print "111111111111111111111111111111111111"
			self.partner_ref=self.amount_tax
			print self.t_tax
			print "111111111111111111111111111111111111"
	def calculateTaxAmount(self, taxes, qty, price_unit):
		amount_tax = 0
		child_tax = 0
		for tax in taxes:
			if tax.enable_child_tax:
				if tax.children_tax_ids:
					child_tax = 0
					for childtax in tax.children_tax_ids:
						child_amount_tax = qty * price_unit * (childtax.amount/100) * (tax.amount/100)
		
						child_tax = child_tax + child_amount_tax 
					parent_tax = qty * price_unit * (tax.amount /100)
					amount_tax = child_tax + parent_tax
			else:
				amount_tax += qty * price_unit * (tax.amount /100)
		
		return amount_tax

