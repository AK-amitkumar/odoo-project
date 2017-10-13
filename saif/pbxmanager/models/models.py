 #-*- coding: utf-8 -*-

from odoo import models, fields, api

class pbxmanager(models.Model):
     _name = 'pbxmanager.pbxmanager'

     callsubject = fields.Char()
     sourcenumber = fields.Char()
     destination = fields.Char()
     notes = fields.Text()
     calldirection = fields.Selection([('Inbound', 'Inbound'), ('Outbound', 'Outbound')])
     callstatus = fields.Selection([('Busy', 'Busy'), ('Answered', 'Answered'), ('Not_answered', 'Not_answered'), ('Failed', 'Failed')])
     callstartdate = fields.Datetime()
     callenddate = fields.Datetime()
     callduration = fields.Integer()
     callrecord =  fields.Text()
     calluid = fields.Text()
     callrelate =  fields.Many2one('res.users',ondelete='set null', string="User", index=True,store=True)
     calldassinged = fields.Many2one('res.partner',ondelete='set null', string="Customer", index=True,store=True)
	 
	 
class usersInherited(models.Model):
    _inherit = 'res.users' 

    x_extension = fields.Char(string='User Extension')
     