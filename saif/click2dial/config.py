from openerp import models, fields, api

class AsteriskConfig(models.TransientModel):
	_inherit = 'base.config.settings'
	_name = 'asterisk.config'

	password = fields.Char()

	@api.multi
	def set_db_password(self):
		password = self[0].password or ''
		self.env['ir.config_parameter'].set_param('password', password)

	@api.multi
	def get_default_credentials(self, fields=None):
		get_param = self.env['ir.config_parameter'].get_param
		password = get_param('password', default='')
		return {
			'password': password
		}