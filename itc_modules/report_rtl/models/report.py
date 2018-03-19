# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 Mohammed M. Hagag.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from odoo import models, fields, api
from odoo.tools.translate import _
import odoo
from odoo.http import request
import lxml.html
import time
import logging
import re
import time
import base64
import logging
import tempfile
import lxml.html
import os
import subprocess
from contextlib import closing
from distutils.version import LooseVersion
from functools import partial
from pyPdf import PdfFileWriter, PdfFileReader

class Report(models.Model):

    _inherit = 'report'
    
    def render(self, cr, uid, ids, template, values=None, context=None):

        if values is None:
            values = {}

        if context is None:
            context = {}
        
        context = dict(context, inherit_branding=True)  # Tell QWeb to brand the generated html

        view_obj = self.pool['ir.ui.view']

        def translate_doc(doc_id, model, lang_field, template):
            return self.translate_doc(cr, uid, doc_id, model, lang_field, template, values, context=context)
        
        ctx = context.copy()
        model=values['doc_model']
        doc_id=values['doc_ids'][0]
        doc = self.pool[model].browse(cr, uid, doc_id, context=ctx)
        
        try:
             lang = str(doc.partner_id.lang)
        except AttributeError:
             lang = context.get('lang')
            
        lang_id = self.pool['res.lang'].search(cr, uid, 
                    [('code', '=', lang),('active','=',True)], context=context)
        lang_obj = self.pool['res.lang'].browse(cr, uid, lang_id, context=context)
        lang_dir = str(lang_obj.direction)
        
        values['lang_dir'] = lang_dir


        user = self.pool['res.users'].browse(cr, uid, uid)
        website = None
        if request and hasattr(request, 'website'):
            if request.website is not None:
                website = request.website
                context = dict(context, translatable=context.get('lang') != request.website.default_lang_code)
        
        values.update(
            time=time,
            context_timestamp=lambda t: fields.datetime.context_timestamp(cr, uid, t, context),
            translate_doc=translate_doc,
            editable=True,
            user=user,
            res_company=user.company_id,
            website=website,
        )
        return view_obj.render(cr, uid, template, values, context=context)
    
    