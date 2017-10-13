# -*- coding: utf-8 -*- 
from odoo import models, fields, api

class OK_PurchaseExtension(models.Model):
	_inherit = 'purchase.order'

	veh_no = fields.Char("Vehical No.")
	location = fields.Char("Location")
	ship = fields.Char("Shipping Address")

	dlv_method = fields.Selection([
		('pick', 'Self Pickup'),
		('dlv', 'Delivered'),
		],default='pick',string="Delivery Method",)

	@api.onchange('dlv_method')	
	def Method(self):
		self.ship = ''



