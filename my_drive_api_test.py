from g_api_utils import get_service, DriveEntry, GmailEntry

de = DriveEntry(readonly=True, metadata=True)
ge = GmailEntry()

drive_service = get_service(de)
gmail_service = get_service(ge)

results = drive_service.files().list(
    pageSize=10,fields="nextPageToken, files(id, name)").execute()

items = results.get('files', [])

if not items:
    print('No files found.')
else:
    print('Files:')
    for item in items:
        print('{0} ({1})'.format(item['name'], item['id']))