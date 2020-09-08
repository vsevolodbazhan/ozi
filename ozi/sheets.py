__all__ = ["setup_service", "extract_values"]

import json

import apiclient.discovery
import httplib2
from django.conf import settings
from oauth2client.service_account import ServiceAccountCredentials


def setup_service():
    apis_list = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]
    try:
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            settings.SHEETS_CREDENTIALS_FILE, apis_list
        )
    except FileNotFoundError:
        credentials_data = json.loads(settings.SHEETS_CREDENTIALS_JSON)
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
