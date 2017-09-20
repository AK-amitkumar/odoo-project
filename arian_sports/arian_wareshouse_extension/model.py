# -*- coding: utf-8 -*- 
from odoo import models, fields, api

class carton_labels(models.Model): 
    _inherit = 'stock.pack.operation' 


    carton_label = fields.Char()

