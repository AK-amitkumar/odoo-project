# -*- coding: utf-8 -*- 
from odoo import models, fields, api

class OK_PurchaseExtension(models.Model):
	_inherit = 'sale.order'
	dlv_tree     = fields.One2many('dip.dlv','dlv_link')
	rcv_tree     = fields.One2many('dip.rcv','rcv_link')



class dip_dlv(models.Model):
	_name = 'dip.dlv'

	ch_no=fields.Char("Ch No. ")
	qty_ltr=fields.Char("Qty Ltr ")
	dip_mm=fields.Char("Dip MM ")
	dlv_link     = fields.Many2one('sale.order')

class dip_rcv(models.Model):
	_name = 'dip.rcv'

	ch_no=fields.Char("Ch No. ")
	qty_ltr=fields.Char("Qty Ltr ")
	dip_mm=fields.Char("Dip MM ")
	rcv_link     = fields.Many2one('sale.order')