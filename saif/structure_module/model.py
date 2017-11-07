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

	






