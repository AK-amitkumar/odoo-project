# -*- coding: utf-8 -*-
import psycopg2
import os


from odoo import models, fields, api

class DashTest(models.Model):
	_inherit = 'dash.test'

    a = fields.Char(string="Style A")
    b = fields.Char(string="Style B")
    c = fields.Char(string="Style C")
    d = fields.Char(string="Style D")
    e = new_field_id = fields.Many2one(comodel_name="", string="", required=False, )
class NewModule(models.Model):
    _name = 'new_module.new_module'
    _rec_name = 'name'
    _description = 'New Description'

    name = fields.Char()
from odoo import api, fields, models
new_field = fields.Date(string="", required=False, )

from odoo import api, fields, models

class NewModule(models.Model):
    _name = 'new_module.new_module'
    _rec_name = 'name'
    _description = 'New Description'

    name = fields.Char()

    @api.onchange('field_name')
    def onchange_method(self):
        self.field_name = ''

@api.onchange('FIELD_NAME')
def _onchange_FIELD_NAME(self):
    pass