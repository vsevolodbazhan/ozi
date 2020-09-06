import apiclient.discovery
import httplib2
from oauth2client.service_account import ServiceAccountCredentials

CREDENTIALS_FILE = "creds.json"


def setup_service(credentials_file=CREDENTIALS_FILE):
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        credentials_file,
        [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ],
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
