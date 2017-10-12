# -*- coding: utf-8 -*- 
import os

from odoo import models, fields, api

class click2dial(models.Model):
	_inherit = 'res.partner'

	passwd = fields.Char("sudo Password")

	@api.multi
	def call(self):	
		get_param = self.env['ir.config_parameter'].get_param
		sudoPassword = get_param('password', default='')
		print sudoPassword
		command = 'asterisk -rvvvx "\originate SIP/205 extension %s@users\"' % (self.phone)
		os.system('echo %s|sudo -S %s' % (sudoPassword, command))

