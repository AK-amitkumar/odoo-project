from __future__ import print_function
# import sqlite3
import time
import uuid
from googleapiclient import errors
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

SCOPES = 'https://www.googleapis.com/auth/drive'
store = file.Storage('/home/odoo/odoo-dev/Projects/saif/google_api_integreation/storage.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('/home/odoo/odoo-dev/Projects/saif/google_api_integreation/client_id.json', SCOPES)
    creds = tools.run_flow(flow, store)
SHEETS = build('sheets', 'v4', http=creds.authorize(Http()))

data = {'properties': {'title': 'Odoo Sheets [%s]' % time.ctime()}
				}
res = SHEETS.spreadsheets().create(body=data).execute()
SHEET_ID = res['spreadsheetId']

service = build('drive', 'v2', http=creds.authorize(Http()))

new_permission = {
	'value': 'default',
	'type': 'anyone',
	'role': 'writer'
	}
try:
  	service.permissions().insert(
      fileId=SHEET_ID, body=new_permission).execute()
except errors.HttpError, error:
  	print ('An error occurred: %s' % error)

media_body = MediaFileUpload('Doc.txt',mimetype='text/plain',resumable=True)
bodyy = {
	'title':'My TEST Doc',
	'description':'A TEST FILE',
	'mimetype':'text/plain'
} 
file =  service.files().insert(body=bodyy,media_body=media_body).execute()
            
# sheets = build('sheets', 'v4', http=creds.authorize(Http()))
# body = {'properties': {'title': 'Odoo [%s]' % time.ctime()}}
# res = sheets.spreadsheets().create(body=body).execute()
# # spreadsheer = Spreadsheet(res, http=creds.authorize(Http()))
# res.set_permissions(anyone=anyone, writers=writers,readers=readers)




print('Created "%s"' % res['properties']['title'])
print ("https://docs.google.com/spreadsheets/d/"+SHEET_ID+"/edit#gid=0")

# url="https://docs.google.com/spreadsheets/d/"+SHEET_ID+"/edit#gid=0"
# webbrowser.open_new_tab(url)

# open a public URL, in this case, the webbrowser docs
# url = "https://docs.google.com/spreadsheets/d/"+SHEET_ID+"/edit#gid=0"

# open an HTML file on my own (Windows) computer
# url = "file://X:/MiscDev/language_links.html"
# webbrowser.open(url,new=new)


# FIELDS = ('ID', 'Customer Name', 'Product Code', 'Units Ordered',
#         'Unit Price', 'Status', 'Created at', 'Updated at')
# cxn = sqlite3.connect('db.sqlite')
# cur = cxn.cursor()
# rows = cur.execute('SELECT * FROM orders').fetchall()
# cxn.close()
# rows.insert(0, FIELDS)