"""
Description:
    Implementation client Google sheet API
"""
from __future__ import print_function
import os.path
import os

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']


Colors = [{"red": 1, "green": 0, "blue": 0}]


def fetch_service():
    """fetch the google service object

    Args:


    Returns:
        Google services object
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


def create_spreadsheet(service, title, sheets_names):
    """Create a new speadsheet

    Args:
        service: Google Services object
        title: Title of the spreadsheet
        sheets_names: list with all names for tabs

    Returns:
        spreadsheet ID
    """
    sheets = []
    counter = 0
    for sheet in sheets_names:
        sheet_info = {
                'properties': {
                    "sheetId": counter,
                    "title": sheet,
                    "index": counter,
                    "tabColor": Colors[0]
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


def write_single(service, spreadsheet_id, range, values):
    """Write in the spreadsheet

    Args:
        service: Google services object
        spreadsheet_id: spreadsheet ID
        range: range of cell where to write, using A1 notation
        values: the information to be written in the spreadsheet

    Returns:
        string confirmation with amount of cells modified
    """
    values = generate_values(values)
    body = {
        'values': values
    }
    result = service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range=range,
        valueInputOption='RAW',
        body=body
    ).execute()
    print(f"{result.get('updatedCells')} cells updated.\n range: {range}")


#TODO: This funtion use the items of the mews articles to create the columns in the spread sheet do i need to hard code it?
def generate_values(raw_data):
    """Take the raw data from newsapi and divided in columns & values, create a list of list containing the information.

    Args:
        raw_data: raw data.

    Returns:
        list of list, first item is the columns names, following lists is the data of the articles.
    """

    news = [list(value.values()) for _, value in raw_data.items()]
    try:
        columns = list(raw_data[1].keys())
    except KeyError:
        columns = ["source", "author", "title", "description", "url", "publishedAt"]
    return [columns] + news


def update_sheet(services, spreadsheet_id, sheet_id, news_title):
    """ Update the spreadsheet

    """

    requests = list()
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
        spreadsheetId=spreadsheet_id,
        body=body
    ).execute()

    print(f'Sheet updated {response}')
