# -*- coding: utf-8 -*-

from openerp import models, fields, api


class mrp_production(models.Model):
    _inherit = "mrp.production"

    # @api.one
    # def action_cancel(self):
    #     for production in self:
    #         if production.state == 'confirmed':
    #             self.write({'state': 'draft'})
    #         elif production.state == 'ready':
    #             self.write({'state': 'draft'})



