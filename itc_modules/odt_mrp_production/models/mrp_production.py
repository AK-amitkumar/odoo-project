# -*- coding: utf-8 -*-

from openerp import models, api


class mrp_production(models.Model):
    _inherit = "mrp.production"

    # override function action_cancel in mrp.production

    # @api.one
    # def action_cancel(self):
    #     move_obj = self.env['stock.move']
    #     for production in self:
    #         if production.state == 'in_production':
    #             consumed_products = [x for x in production.move_lines2]  # print consumed product
    #             for product in consumed_products:
    #                 stock = move_obj.create({
    #                     'name': product.product_id.name,
    #                     'product_id': product.product_id.id,
    #                     'restrict_lot_id': product.restrict_lot_id.id,
    #                     'product_uom_qty': product.product_uom_qty,
    #                     'product_uom': product.product_uom.id,
    #                     'partner_id': product.product_uom.id,
    #                     'location_id': product.location_dest_id.id,
    #                     'location_dest_id': product.location_id.id,
    #                 })
    #                 stock.action_done()
    #     return super(mrp_production, self).action_cancel()
