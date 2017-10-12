from __future__ import print_function
# import sqlite3
import time

from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import psycopg2
import webbrowser


# SCOPES = ('https://www.googleapis.com/auth/drive')
# store = file.Storage('storage.json')
# creds = store.get()
# if not creds or creds.invalid:
#     flow = client.flow_from_clientsecrets('client_id.json', SCOPES)
#     creds = tools.run_flow(flow, store)
# SHEETS = discovery.build('docs', 'v4', http=creds.authorize(Http()))

# data = {'properties': {'title': 'Toy orders [%s]' % time.ctime()}}
# res = SHEETS.document().create(body=data).execute()
# SHEET_ID = res['documentId']
# print('Created "%s"' % res['properties']['title'])



SCOPES = 'https://www.googleapis.com/auth/drive'
store = file.Storage('storage.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_id.json', SCOPES)
    creds = tools.run_flow(flow, store)
SHEETS = build('sheets', 'v4', http=creds.authorize(Http()))

data = {'properties': {'title': 'Toy orders [%s]' % time.ctime()}}
res = SHEETS.spreadsheets().create(body=data).execute()
SHEET_ID = res['spreadsheetId']
print('Created "%s"' % res['properties']['title'])

try:
	conn = psycopg2.connect("dbname='champion_db' user='postgres' host='localhost' password='odoo'")
except:
	print ("I am unable to connect to the database")
cur = conn.cursor()
cur.execute('SELECT * FROM account_invoice')
rows =cur.fetchall()
data = {'values': [row[19:27] for row in rows]}

SHEETS.spreadsheets().values().update(spreadsheetId=SHEET_ID,
    range='A1', body=data, valueInputOption='RAW').execute()

print('Wrote data to Sheet:')

rows = SHEETS.spreadsheets().values().get(spreadsheetId=SHEET_ID,
    range='Sheet1').execute().get('values', [])
for row in rows:
    print(row)

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