# -*- coding: utf-8 -*- 
from __future__ import print_function
import time
from googleapiclient.discovery import build
from googleapiclient import errors
from httplib2 import Http
from oauth2client import file, client, tools
from odoo import models, fields, api

class Google_docs_integration(models.Model):
	
	
	_name = 'google.inte'
	_rec_name = 'uidd'
	
	doc_ref = fields.Char("Name" )
	uidd = fields.Char()
	doc_name = fields.Char("Document Name" , required=True)
	proj = fields.Many2one('project.project',string="Project")
	hide_button = fields.Boolean()
	doc_link = fields.Char("Google Doc Link")
	doc_type = fields.Selection([
		('Spreadsheet', 'Odoo Spreadsheet'),
		('Document', 'Odoo Document'),
		('Presentation', 'Odoo Presentation'),
		],default='Spreadsheet',string="Document Type" , required=True)

 	File_ID = ''


	@api.model 
	def create(self, vals):
		vals['doc_ref'] = self.env['ir.sequence'].next_by_code('dem.seq')
		new_record = super(Google_docs_integration, self).create(vals) 
		return new_record
	
	@api.multi
	def create_doc(self):
		SCOPES = 'https://www.googleapis.com/auth/drive'
		store = file.Storage('/home/odoo/odoo-dev/Projects/saif/google_api_integreation/storage.json')
		creds = store.get()
		if not creds or creds.invalid:
			flow = client.flow_from_clientsecrets('/home/odoo/odoo-dev/Projects/saif/google_api_integreation/client_id.json', SCOPES)
			creds = tools.run_flow(flow, store)
		drive_service = build('drive', 'v3', http=creds.authorize(Http()))
		if self.doc_type == 'Spreadsheet':

			file_metadata = {
			    'name': "[%s] [%s]" %( self.doc_name , time.ctime()),
			    'mimeType': 'application/vnd.google-apps.spreadsheet'
			}
		elif self.doc_type == 'Presentation':

			file_metadata = {
			    'name': "[%s] [%s]" %( self.doc_name , time.ctime()),
			    'mimeType': 'application/vnd.google-apps.presentation'
			}
		else:

			file_metadata = {
			    'name': "[%s] [%s]" %( self.doc_name , time.ctime()),
			    'mimeType': 'application/vnd.google-apps.document'
			}

		filee = drive_service.files().create(body=file_metadata,
			                                    fields='id').execute()
		self.File_ID = filee.get('id')

		self.changePermissions()
		self.ref()

	def changePermissions(self):
		SCOPES = 'https://www.googleapis.com/auth/drive'
		store = file.Storage('/home/odoo/odoo-dev/Projects/saif/google_api_integreation/storage.json')
		creds = store.get()
		if not creds or creds.invalid:
			flow = client.flow_from_clientsecrets('/home/odoo/odoo-dev/Projects/saif/google_api_integreation/client_id.json', SCOPES)
			creds = tools.run_flow(flow, store)
		drive_service = build('drive', 'v3', http=creds.authorize(Http()))

		new_permission = {
	    'value': 'default',
	    'type': 'anyone',
	    'role': 'writer'
		    }
		try:
		    drive_service.permissions().create(
		        fileId=self.File_ID,
		        body=new_permission,).execute()
		except errors.HttpError, error:
		    print ('An error occurred: %s' % error)

		if self.doc_type == 'Spreadsheet':
			self.doc_link = "https://docs.google.com/spreadsheets/d/"+self.File_ID+"/edit#gid=0"
		
		elif self.doc_type == 'Presentation':
			self.doc_link = "https://docs.google.com/presentation/d/"+self.File_ID+"/edit#slide=id.p"
		
		else:
			self.doc_link = "https://docs.google.com/document/d/"+self.File_ID+"/edit"
		self.hide_button = True

	def ref(self):
		customer = self.env['res.users'].search([('id','=',self._uid)])
		self.uidd = self.doc_type +' /'+  customer.name +' /'+ self.doc_ref


	@api.multi
	def open_doc(self):
		return {
			'name'     : 'Odoo Google Docs',
			'res_model': 'ir.actions.act_url',
			'type'     : 'ir.actions.act_url',
			'target'   : 'current',	
			'url'		: self.doc_link,
		}	