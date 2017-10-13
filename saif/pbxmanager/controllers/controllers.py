# -*- coding: utf-8 -*-
from odoo import http

class pbxmanager(http.Controller):
     @http.route('/pbxmanager/pbxmanager/', auth='public')
     def index(self, **kw):
         return "Hello, world"

     @http.route('/pbxmanager/pbxmanager/objects/', auth='public')
     def list(self, **kw):
         return http.request.render('pbxmanager.listing', {
             'root': '/pbxmanager/pbxmanager',
             'objects': http.request.env['pbxmanager.pbxmanager'].search([]),
         })

     @http.route('/pbxmanager/pbxmanager/objects/<model("pbxmanager.pbxmanager"):obj>/', auth='public')
     def object(self, obj, **kw):
         return http.request.render('pbxmanager.object', {
             'object': obj
         })