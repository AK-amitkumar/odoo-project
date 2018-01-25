# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import time
from googleapiclient.discovery import build
from googleapiclient import errors
from googleapiclient.http import MediaFileUpload
from httplib2 import Http
from oauth2client import file, client, tools
import config
from odoo import models, fields, api

class Google_docs_integration(models.Model):
	
	
	_name = 'google.inte'
	_rec_name = 'doc_ref'
	
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

	img = fields.Binary(string="Images",  )
	first_attachment_ids =fields.One2many(
		comodel_name='max.base.multi.attachment', inverse_name='owner_id', string='First Attachments',
		domain=lambda self: [('owner_model', '=', self._name), ('owner_field', '=', 'first_attachment_ids')], copy=True)
	second_attachment_ids = fields.One2many(
		comodel_name='max.base.multi.attachment', inverse_name='owner_id', string='Second Attachments',
		domain=lambda self: [('owner_model', '=', self._name), ('owner_field', '=', 'second_attachment_ids')],
		copy=True)

	File_ID = ''

	@api.model
	def install(self):
		""" when module insatll run terminal command in it"""
		# os.system('sudo apt-get update')
		# sudoPassword = 'odoo'
		# command = 'sudo pip install --upgrade google-api-python-client'
		# os.system('echo %s| sudo -S %s' % (sudoPassword, command))
		command = 'pip install --upgrade google-api-python-client'
		os.system('echo %s' % command)

	@ api.model
	def create(self, vals):
		seq = self.env['ir.sequence'].next_by_code('dem.seq')
		customer = self.env['res.users'].search([('id','=',self._uid)])
		vals['doc_ref'] = vals['doc_name'] +' /'+  customer.name +' /'+ seq
		new_record = super(Google_docs_integration, self).create(vals)
		return new_record
	
	def create_drive_link(self):
		SCOPES = config.urls['scope']
		store = file.Storage(config.urls['storage'])
		creds = store.get()
		if not creds or creds.invalid:
			flow = client.flow_from_clientsecrets(config.urls['client_id'], SCOPES)
			creds = tools.run_flow(flow, store)
		return build('drive', 'v3', http=creds.authorize(Http()))


	@api.multi
	def upload_doc(self):
		drive_service = self.create_drive_link()
		file_metadata = {
			'name': 'My Report',
			'mimeType': 'application/vnd.google-apps.file'
		}
		media = MediaFileUpload('/home/muhammad/file.csv',
								mimetype='text/csv',
								resumable=True)
		file = drive_service.files().create(body=file_metadata,
											media_body=media,
											fields='id').execute()
		print('File ID: %s' % file.get('id'))

	@api.multi
	def create_doc(self):

		drive_service = self.create_drive_link()
		if self.doc_type == 'Spreadsheet':

			file_metadata = {
				'name': "[%s] [%s]" %( self.doc_name , time.ctime()),
				'mimeType': config.urls['mimeType']+'spreadsheet'
			}
		elif self.doc_type == 'Presentation':

			file_metadata = {
				'name': "[%s] [%s]" %( self.doc_name , time.ctime()),
				'mimeType': config.urls['mimeType']+'presentation'
			}
		else:

			file_metadata = {
				'name': "[%s] [%s]" %( self.doc_name , time.ctime()),
				'mimeType': config.urls['mimeType']+'document'
			}

		if not(self.doc_link):
			filee = drive_service.files().create(body=file_metadata,
				                                    fields='id').execute()
			self.File_ID = filee.get('id')
			self.changePermissions()
			return self.open_doc()

	def changePermissions(self):

		drive_service = self.create_drive_link()
		new_permission = {
		'value': 'default',
		'type': 'anyone',
		'role': 'writer'
			}
		try:
			drive_service.permissions().create(fileId=self.File_ID,
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

	@api.multi
	def open_doc(self):
		return {
			'name'     : 'Odoo Google Docs',
			'res_model': 'ir.actions.act_url',
			'type'     : 'ir.actions.act_url',
			'target'   : 'current',	
			'url'		: self.doc_link,
		}

	@api.multi
	def unlink(self):
		drive_service = self.create_drive_link()
		for rec in self:
			if rec.doc_link:
				File_ID = rec.doc_link.split('/')[-2]
				del_file = drive_service.files().delete(fileId = File_ID).execute()
		re =super(Google_docs_integration, self).unlink()
		return re

class task_extension(models.Model):
	_inherit = 'project.task'

	doc = fields.Many2one('google.inte',string='Document')