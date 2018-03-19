# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Tax_Number_customer(models.Model):
    _inherit = 'res.partner'

    tax_number = fields.Char('Tax Number')