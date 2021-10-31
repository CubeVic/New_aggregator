from __future__ import print_function
import os.path
from typing import List, Dict, Union, Any

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import datetime

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive']


def fetch_service():
    """Shows basic usage of the Sheets API.
        Prints values from a sample spreadsheet.
        """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('sheets', 'v4', credentials=creds)
    return service


# def create_spreadsheet(service, title):
#     spreadsheet = {
#         'properties': {
#             'title': title
#         },
#         'sheets': [
#             {
#                 'properties': {
#                     "sheetId": 0,
#                     "title": 'first_sheet',
#                     "index": 0,
#                 }
#             }
#         ]
#     }
#
#     spreadsheet = service.spreadsheets().create(body=spreadsheet, fields='spreadsheetId').execute()
#     return spreadsheet.get('spreadsheetId')


def create_spreadsheet(service, title, sheets_names):
    sheets = []
    counter = 0
    for sheet in sheets_names:
        sheet_info = {
                'properties': {
                    "sheetId": counter,
                    "title": sheet,
                    "index": counter,
                }
            }
        counter += 1
        sheets.append(sheet_info)

    spreadsheet = {
        'properties': {
            'title': title
        },
        'sheets': sheets
    }

    spreadsheet = service.spreadsheets().create(body=spreadsheet, fields='spreadsheetId').execute()
    return spreadsheet.get('spreadsheetId')


def write_single(service, spreadsheet_ID, range, values):
    values = generate_values(values)
    body = {
        'values': values
    }
    result = service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_ID,
        range=range,
        valueInputOption='RAW',
        body=body
    ).execute()
    print(f"{result.get('updatedCells')} cells updated.\n range: {range}")


def generate_values(raw_data):
    news = [list(value.values()) for _, value in raw_data.items()]
    columns = list(raw_data[1].keys())
    return [columns] + news


def update_sheet(services, SPREADSHEET_ID, sheet_id, news_title):

    requests = []
    requests.append({
        'updateSheetProperties': {
            'properties': {
                'sheetId': sheet_id,
                'title': news_title
            },
            'fields': 'title'
        }
    })

    body = {
        'requests': requests
    }

    response = services.spreadsheets().batchUpdate(
        spreadsheetId=SPREADSHEET_ID,
        body=body
    ).execute()
    # find_replace_response = response
    print(f'Sheet updated {response}')

