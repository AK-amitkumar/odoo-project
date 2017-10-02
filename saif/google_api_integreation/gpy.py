import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json



scope = ['https://spreadsheets.google.com/feeds']
credentials = ServiceAccountCredentials.from_json_keyfile_name('client_id.json', scope)
gc = gspread.authorize(credentials)
wks = gc.open("Odoo").sheet1
glist = wks.get_all_values()



print(glist)

https://docs.google.com/spreadsheets/d/1bY0H6KIHrScQVhGH1Wgpp0HOBUt5H17rFoncf_dDeOg/edit?usp=sharing