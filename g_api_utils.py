from __future__ import print_function

import os
from os import path
import httplib2

import oauth2client
from oauth2client import client, tools
from apiclient import discovery

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

## File name built in the ~/.credentials directory when credentials_path is called
CREDENTIALS_FILE_NAME = 'pydaemon-client.json'

AUTH_LINK_ROOT = 'https://www.googleapis.com/auth'
## TODO: Edit this path to your client secret file location
client_secrets_dir = 'C:\\Dev\\api_credentials\\google'
CLIENT_SECRET_FILE = path.join(client_secrets_dir, 'pydaemon_client_secret.json')
APPLICATION_NAME = 'Py Daemon Test'

def linkjoin(*link_eleemnts):
    return '/'.join(link_eleemnts)

def dotjoin(*strings):
    return '.'.join(strings)


class _APIEntry():
    '''
    Convenience class for accessing different Google APIs.
    Pass into get_service to get the discovery.build() result of the given API.

    Attributes:
        build_name (str):   Pass this attribute into the 'serviceName' argument of apiclient.discovery.build()
                            Done automatically when instance of this object is passed into get_service()
        build_v (str):      Pass this attribute into the 'version' argument of apiclient.discovery.build()
                            Done automatically when instance of this object is passed into get_service()
        scope (str):        Set based on constructor arguments passed in.
                            Pass this into oauth2.client.flow_from_clientsecrets with the client secret file for access.
                            Done automatically when instance of this object is passed into get_service()

    '''

    build_name = None
    build_v = None
    def __init__(self):
        self.scope = None


class DriveEntry(_APIEntry):
    '''
    Convenience entry class for connecting to the Drive API.
    Pass into get_service to get the discovery.build() result of this API.

    SCOPES:

    https://www.googleapis.com/auth/drive
    https://www.googleapis.com/auth/drive.appdata
    https://www.googleapis.com/auth/drive.file
    https://www.googleapis.com/auth/drive.metadata
    https://www.googleapis.com/auth/drive.metadata.readonly
    https://www.googleapis.com/auth/drive.photos.readonly
    https://www.googleapis.com/auth/drive.readonly
    https://www.googleapis.com/auth/drive.scripts
    '''

    build_name = 'drive'
    build_v = 'v3'



    SPECIAL_OPTIONS = ('file', 'photos', 'script', 'appdata')

    def __init__(self, readonly=True, metadata=False, special=None):
        ''' special overrides all other arguments if not None (See self.SEPCIAL_OPTIONS).
        Otherwise, readonly and metadata each be switched off or on in any combination.'''
        link_root = linkjoin(AUTH_LINK_ROOT, 'drive')
        '''
        if len([x for x in (file, photos, scripts, appdata) if x]) > 1:
            raise ValueError("Can't set more than one of photos, scripts, file and appdata as true.  Any one of these set to true override all other arguments")
        '''
        if special is not None:
            if special == 'file':
                self.scope = dotjoin(link_root, 'file')
                return
            elif special == 'photos':
                self.scope = dotjoin(link_root, 'photos', 'readonly')
                return
            elif special == 'scripts':
                self.scope = dotjoin(link_root, 'scripts')
                return
            elif special == 'appdata':
                self.scope = dotjoin(link_root, 'appdata')
                return
            else:
                raise ValueError('special argument must be either None (default) or one of {}.'.format(self.SPECIAL_OPTIONS))
        else:
            scope = link_root
            if metadata:
                scope = dotjoin(scope, 'metadata')
            if readonly:
                scope = dotjoin(scope, 'readonly')

            self.scope = scope

class CalEntry(_APIEntry):
    '''
    Convenience entry class for connecting to the Calendar API.
    Pass into get_service to get the discovery.build() result of this API.

    SCOPES:

    https://www.googleapis.com/auth/calendar
    https://www.googleapis.com/auth/calendar.readonly
    '''

    build_name = 'calendar'
    build_v = 'v1'



    def __init__(self, readonly=True):
        link_root = linkjoin(AUTH_LINK_ROOT, 'calendar')
        scope = link_root
        if readonly:
            scope = dotjoin(scope, 'readonly')

        self.scope = scope

class GmailEntry(_APIEntry):
    '''
    Convenience entry class for connecting to the Gmail API.
    Pass into get_service to get the discovery.build() result of this API.

    SCOPES:

    https://www.googleapis.com/auth/drive
    https://www.googleapis.com/auth/drive.appdata
    https://www.googleapis.com/auth/drive.file
    https://www.googleapis.com/auth/drive.metadata
    https://www.googleapis.com/auth/drive.metadata.readonly
    https://www.googleapis.com/auth/drive.photos.readonly
    https://www.googleapis.com/auth/drive.readonly
    https://www.googleapis.com/auth/drive.scripts
    '''

    build_name = 'gmail'
    build_v = 'v1'

    SPECIAL_OPTIONS = ('compose', 'insert', 'modify', 'send', 'settings.basic', 'settings.sharing')

    def __init__(self, readonly=True, special=None):
        ''' special overrides all other arguments if not None (See self.SEPCIAL_OPTIONS).
        Otherwise, readonly can be switched off or on.'''

        link_root = linkjoin(AUTH_LINK_ROOT, 'gmail')
        if special is not None:
            if special in self.SPECIAL_OPTIONS:
                self.scope = dotjoin(link_root, special)
                return
            else:
                raise ValueError('special argument must be either None (default) or one of {}.'.format(self.SPECIAL_OPTIONS))
        elif readonly:
            self.scope = dotjoin(link_root, 'readonly')
        else:
            self.scope = 'https://mail.google.com/'


class AnalyticsEntry(_APIEntry):
    '''
    Convenience entry class for connecting to the Analytics API.
    Pass into get_service to get the discovery.build() result of this API.

    SCOPES:

    https://www.googleapis.com/auth/analytics
    https://www.googleapis.com/auth/analytics.edit
    https://www.googleapis.com/auth/analytics.manage.users
    https://www.googleapis.com/auth/analytics.manage.users.readonly
    https://www.googleapis.com/auth/analytics.provision
    https://www.googleapis.com/auth/analytics.readonly
    '''

    build_name = 'analytics'
    build_v = 'v3'

    SPECIAL_OPTIONS = ('edit', 'provision')




    def __init__(self, readonly=True, manage_users=False, special=None):
        ''' special overrides all other arguments if not None (See self.SEPCIAL_OPTIONS).
        Otherwise, readonly and manage_users each be switched off or on in any combination.'''
        link_root = linkjoin(AUTH_LINK_ROOT, 'analytics')
        if special is not None:
            if special in self.SPECIAL_OPTIONS:
                self.scope = dotjoin(link_root, special)
                return
            else:
                raise ValueError('Special argument must be either None (default) or one of {}.'.format(self.SPECIAL_OPTIONS))
        else:
            scope = link_root
            if manage_users:
                scope = dotjoin(scope, 'manage', 'users')
            if readonly:
                scope = dotjoin(scope, 'readonly')
            self.scope = scope

'''
class ActivityEntry():
    build_name
'''

def credentials_path():
    ''' Builds ~/.credentials directory and returns joined path of that and CREDENTIALS_FILE_NAME, which is used
        as the argument for oauth2client.file.Storage()'''
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   CREDENTIALS_FILE_NAME)
    return credential_path

def get_service(entry_obj):
    '''
    Gets api service based on passed in _APIEntry (DriveEntry, GmailEntry, CalEntry, AnalyticsEntry,) object.

    Based off of a combination of get_credentials and main() from the Google Drive API Quickstart script

    Returns:
        desired service.
    '''


    # credential_path = os.path.join(credential_dir,
    #                               'drive-python-quickstart.json')
    cred_path = credentials_path()
    store = oauth2client.file.Storage(cred_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, entry_obj.scope)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:  # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + cred_path)

    http = credentials.authorize(httplib2.Http())
    service = discovery.build(entry_obj.build_name, entry_obj.build_v, http=http)
    return service

'''
# TODO: Remove if get_service works well
def get_credentials(entry_obj):
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'pydaemon-client.json')

    #credential_path = os.path.join(credential_dir,
    #                               'drive-python-quickstart.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, entry_obj.scope)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials
'''