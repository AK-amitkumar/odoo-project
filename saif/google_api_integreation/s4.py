from __future__ import print_function

from googleapiclient.discovery import build
from httplib2 import Http
import time
from oauth2client import file, client, tools
try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/drive'
store = file.Storage('/home/odoo/odoo-dev/Projects/saif/google_api_integreation/storage.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('/home/odoo/odoo-dev/Projects/saif/google_api_integreation/client_id.json', SCOPES)
    creds = tools.run_flow(flow, store)
drive_service = build('drive', 'v3', http=creds.authorize(Http()))

file_metadata = {
    'name': "Odoo Spreadsheet [%s]" % time.ctime(),
    'mimeType': 'application/vnd.google-apps.spreadsheet'
}

# file_metadata = {
#     'name': "Odoo Presentation [%s]" % time.ctime(),
#     'mimeType': 'application/vnd.google-apps.presentation'
# }

# file_metadata = {
#     'name': "Odoo Document [%s]" % time.ctime(),
#     'mimeType': 'application/vnd.google-apps.document'
# }

file = drive_service.files().create(body=file_metadata,
                                    fields='id').execute()
print (file.get('id'))





new_permission = {
    'value': 'default',
    'type': 'anyone',
    'role': 'writer'
    }
try:
    drive_service.permissions().create(
        fileId=file.get('id'),
        body=new_permission,).execute()
except errors.HttpError, error:
    print ('An error occurred: %s' % error)
print('DONE')



# FILES = (
#     ('hello.txt', None),
#     ('hello.txt', 'application/vnd.google-apps.document'),
# )

# for filename, mimeType in FILES:
#     metadata = {'name': filename}
#     if mimeType:
#         metadata['mimeType'] = mimeType


# rsp = SLIDES.documents().create(
#         body={'title': 'Odoo Slides [%s]' % time.ctime()}).execute()

# res = DRIVE.files().create(body={'mimeType':'application/vnd.google-apps.document'}, media_body='Odoo Docs [%s].txt' % time.ctime()).execute()
# if res:
#     print('Uploaded "%s" (%s)' % ("filename", res['mimeType']))

# if res:
#     MIMETYPE = 'application/pdf'
#     data = DRIVE.files().export(fileId=res['id'], mimeType=MIMETYPE).execute()
#     if data:
#         fn = '%s.pdf' % os.path.splitext(filename)[0]
#         with open(fn, 'wb') as fh:
#             fh.write(data)
#         print('Downloaded "%s" (%s)' % (fn, MIMETYPE))