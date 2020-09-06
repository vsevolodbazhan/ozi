import json
import os

import apiclient.discovery
import httplib2
from oauth2client.service_account import ServiceAccountCredentials

CREDENTIALS_FILE = "creds.json"
CREDENTIALS_VARIABLE_NAME = "SHEETS_API_CREDS"


def setup_service(credentials_file=CREDENTIALS_FILE):
    apis_list = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]
    try:
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            credentials_file, apis_list
        )
    except FileNotFoundError:
        credentials_data = json.loads(os.environ[CREDENTIALS_VARIABLE_NAME])
        credentials = ServiceAccountCredentials.from_json_keyfile_dict(
            credentials_data, apis_list
        )
    httpAuth = credentials.authorize(httplib2.Http())
    service = apiclient.discovery.build("sheets", "v4", http=httpAuth)
    return service


def extract_values(spreadsheet_id, column, range_start, range_end):
    service = setup_service()
    data = (
        service.spreadsheets()
        .values()
        .get(
            spreadsheetId=spreadsheet_id,
            range=f"{column}{range_start}:{column}{range_end}",
            majorDimension="COLUMNS",
        )
    ).execute()

    if values := data.get("values"):
        return values[0]
