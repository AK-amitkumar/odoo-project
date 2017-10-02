# -*- coding: utf-8 -*- 
from __future__ import print_function
# import sqlite3
import time

from googleapiclient.discovery import build
from googleapiclient import errors
from httplib2 import Http
from oauth2client import file, client, tools
# import errors
# import psycopg2
import webbrowser
# import s1 as sss
from odoo import models, fields, api

class Google_docs_integration(models.Model):
	
	_name = 'google.inte'
	_rec_name = 'username'
	
	username = fields.Char("UserName" , required=True)
	password = fields.Char("Password" , required=True)
	doc_link = fields.Char("Google Doc Link")
	hide = fields.Boolean()
	SHEET_ID = ''

	# def abc(self):

	# 	SCOPES = 'https://www.googleapis.com/auth/drive'
	# 	store = file.Storage('storage.json')
	# 	creds = store.get()
	# 	if not creds or creds.invalid:
	# 	    flow = client.flow_from_clientsecrets('/home/odoo/odoo-dev/Projects/saif/google_api_integreation/client_id.json', SCOPES)
	# 	    creds = tools.run_flow(flow, store)
	# 	SHEETS = build('sheets', 'v4', http=creds.authorize(Http()))

	# 	data = {'properties': {'title': 'Toy orders [%s]' % time.ctime()}}
	# 	res = SHEETS.spreadsheets().create(body=data).execute()
	# 	SHEET_ID = res['spreadsheetId']
	# 	print('Created "%s"' % res['properties']['title'])

	# 	try:
	# 		conn = psycopg2.connect("dbname='champion_db' user='postgres' host='localhost' password='odoo'")
	# 	except:
	# 		print ("I am unable to connect to the database")
	# 	cur = conn.cursor()
	# 	cur.execute('SELECT * FROM account_invoice')
	# 	rows =cur.fetchall()
	# 	data = {'values': [row[19:27] for row in rows]}

	# 	SHEETS.spreadsheets().values().update(spreadsheetId=SHEET_ID,
	# 	    range='A1', body=data, valueInputOption='RAW').execute()

	# 	print('Wrote data to Sheet:')

	# 	rows = SHEETS.spreadsheets().values().get(spreadsheetId=SHEET_ID,
	# 	    range='Sheet1').execute().get('values', [])
	# 	for row in rows:
	# 	    print(row)

	@api.multi
	def create_doc(self):
		SCOPES = 'https://www.googleapis.com/auth/drive'
		store = file.Storage('/home/odoo/odoo-dev/Projects/saif/google_api_integreation/storage.json')
		creds = store.get()
		if not creds or creds.invalid:
			flow = client.flow_from_clientsecrets('/home/odoo/odoo-dev/Projects/saif/google_api_integreation/client_id.json', SCOPES)
			creds = tools.run_flow(flow, store)
		SHEETS = build('sheets', 'v4', http=creds.authorize(Http()))

		data = {'properties': {'title': 'Odoo [%s]' % time.ctime()}
						}
		res = SHEETS.spreadsheets().create(body=data).execute()
		self.SHEET_ID = res['spreadsheetId']


		self.doc_link = "https://docs.google.com/spreadsheets/d/{0}/edit#gid=0".format(self.SHEET_ID)
		# print self.doc_link
		# print ("https://docs.google.com/spreadsheets/d/"+SHEET_ID+"/edit#gid=0")
			
		self.p_cha()

	def p_cha(self):
		SCOPES = 'https://www.googleapis.com/auth/drive'
		store = file.Storage('/home/odoo/odoo-dev/Projects/saif/google_api_integreation/storage.json')
		creds = store.get()
		if not creds or creds.invalid:
			flow = client.flow_from_clientsecrets('/home/odoo/odoo-dev/Projects/saif/google_api_integreation/client_id.json', SCOPES)
			creds = tools.run_flow(flow, store)
		service = build('drive', 'v2', http=creds.authorize(Http()))
		new_permission = {
			'value': 'default',
			'type': 'anyone',
			'role': 'writer'
			}
		try:
			service.permissions().insert(
			  fileId=self.SHEET_ID, body=new_permission).execute()
		except errors.HttpError, error:
			pass


	@api.multi
	def open_doc(self):
		pass


	@api.onchange('doc_link')
	def btn(self):
		if not self.doc_link:
			self.hide = False
		else:
			self.hide = True