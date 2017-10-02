from __future__ import print_function
import time
import uuid
from googleapiclient.discovery import build
from googleapiclient import errors
from httplib2 import Http
from oauth2client import file, client, tools

gen_uuid = lambda : str(uuid.uuid4())  # get random UUID string

SCOPES = 'https://www.googleapis.com/auth/drive'
store = file.Storage('/home/odoo/odoo-dev/Projects/saif/google_api_integreation/storage.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('/home/odoo/odoo-dev/Projects/saif/google_api_integreation/client_id.json', SCOPES)
    creds = tools.run_flow(flow, store)
SLIDES = build('slides', 'v1', http=creds.authorize(Http()))

print('** Create new slide deck & set up object IDs')
rsp = SLIDES.presentations().create(
        body={'title': 'Odoo Slides [%s]' % time.ctime()}).execute()
deckID = rsp['presentationId']
titleSlide  = rsp['slides'][0]      # title slide object IDs
titleID     = titleSlide['pageElements'][0]['objectId']
subtitleID  = titleSlide['pageElements'][1]['objectId']
mpSlideID   = gen_uuid()            # mainpoint IDs
mpTextboxID = gen_uuid()
smileID     = gen_uuid()            # shape IDs
str24ID     = gen_uuid()
arwbxID     = gen_uuid()

print('** Create "main point" slide, add text & interesting shapes')
reqs = [
    # create new "main point" layout slide, giving slide & textbox IDs
    {'createSlide': {
        'objectId': mpSlideID,
        'slideLayoutReference': {'predefinedLayout': 'MAIN_POINT'},
        'placeholderIdMappings': [{
            'objectId': mpTextboxID,
            'layoutPlaceholder': {'type': 'TITLE', 'index': 0}
        }],
    }},
    # add title & subtitle to title slide; add text to main point slide textbox
    {'insertText': {'objectId': titleID,     'text': 'Odoo Slides'}},
    {'insertText': {'objectId': subtitleID,  'text': 'via the Google Slides API'}},
    {'insertText': {'objectId': mpTextboxID, 'text': 'text & shapes'}}
    ]

SLIDES.presentations().batchUpdate(body={'requests': reqs},
        presentationId=deckID).execute()


service = build('drive', 'v2', http=creds.authorize(Http()))

new_permission = {
    'value': 'default',
    'type': 'anyone',
    'role': 'writer'
    }
try:
    service.permissions().insert(
      fileId=deckID, body=new_permission).execute()
except errors.HttpError, error:
    print ('An error occurred: %s' % error)
print('DONE')