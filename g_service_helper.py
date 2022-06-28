from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/tasks', 'https://www.googleapis.com/auth/calendar.readonly']

def Create_Service(user, api_name, api_version):
    """Creates the service to be used for the apps
    """
    user_token = f"user_info/t_{user}_{api_name}_{api_version}.json"

    creds = None
    if os.path.exists(user_token):
        creds = Credentials.from_authorized_user_file(user_token, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open(user_token, 'w') as token:
            token.write(creds.to_json())
    try:
        service = build(api_name, api_version, credentials=creds)
        return service
    except HttpError as err:
        print(err)

if __name__ == "__main__":
    import sys
    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
    creds = flow.run_local_server(port=0)
    user_token = f"user_info/t_{sys.argv[1]}_{sys.argv[2]}_{sys.argv[3]}.json"
    with open(user_token, 'w') as token:
            token.write(creds.to_json())