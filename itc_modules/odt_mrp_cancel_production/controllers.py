# -*- coding: utf-8 -*-
from openerp import http

# class MrpCancelProduction(http.Controller):
#     @http.route('/odt_mrp_cancel_production/odt_mrp_cancel_production/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/odt_mrp_cancel_production/odt_mrp_cancel_production/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('odt_mrp_cancel_production.listing', {
#             'root': '/odt_mrp_cancel_production/odt_mrp_cancel_production',
#             'objects': http.request.env['odt_mrp_cancel_production.odt_mrp_cancel_production'].search([]),
#         })

#     @http.route('/odt_mrp_cancel_production/odt_mrp_cancel_production/objects/<model("odt_mrp_cancel_production.odt_mrp_cancel_production"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('odt_mrp_cancel_production.object', {
#             'object': obj
#         })