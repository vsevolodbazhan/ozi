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


def extract_values(
    spreadsheet_id, column, range_start, range_end, render_option="FORMULA"
):
    service = setup_service()
    data = (
        service.spreadsheets()
        .values()
        .get(
            spreadsheetId=spreadsheet_id,
            range=f"{column}{range_start}:{column}{range_end}",
            majorDimension="COLUMNS",
            valueRenderOption=render_option,
        )
    ).execute()

    if values := data.get("values"):
        return values[0]


def extract_chats(values):
    prefix = "chats/"
    postfix = '";'

    chats = []
    for value in values:
        start = value.find(prefix) + len(prefix)
        end = value.find(postfix)
        chats.append(value[start:end])

    return chats


def test_extract_chats():
    values = [
        '=HYPERLINK("https://app.tomoru.ru/bot/DMPfEuZ1TEPYDea26gBk/chats/JoL3SuysP0fiBy94e9aO-678295990";"Mikhail")',
        '=HYPERLINK("https://app.tomoru.ru/bot/DMPfEuZ1TEPYDea26gBk/chats/JoL3SuysP0fiBy94e9aO-304277490";"Varvara Bondarenko")',
        '=HYPERLINK("https://app.tomoru.ru/bot/DMPfEuZ1TEPYDea26gBk/chats/JoL3SuysP0fiBy94e9aO-826341750";"L")',
        '=HYPERLINK("https://app.tomoru.ru/bot/DMPfEuZ1TEPYDea26gBk/chats/jmSSJNV8wLWQvooCDxwQ-159638777";"Розалия Абдуллина")',
        '=HYPERLINK("https://app.tomoru.ru/bot/DMPfEuZ1TEPYDea26gBk/chats/jmSSJNV8wLWQvooCDxwQ-185599130";"Далия Исаева")',
        '=HYPERLINK("https://app.tomoru.ru/bot/DMPfEuZ1TEPYDea26gBk/chats/JoL3SuysP0fiBy94e9aO-845289386";"Лола")',
        '=HYPERLINK("https://app.tomoru.ru/bot/DMPfEuZ1TEPYDea26gBk/chats/JoL3SuysP0fiBy94e9aO-544237010";"Rusalena")',
        '=HYPERLINK("https://app.tomoru.ru/bot/DMPfEuZ1TEPYDea26gBk/chats/JoL3SuysP0fiBy94e9aO-304427935";"Hi, Mari.")',
        '=HYPERLINK("https://app.tomoru.ru/bot/DMPfEuZ1TEPYDea26gBk/chats/jmSSJNV8wLWQvooCDxwQ-3385555";"Александра Терентьева")',
        '=HYPERLINK("https://app.tomoru.ru/bot/DMPfEuZ1TEPYDea26gBk/chats/JoL3SuysP0fiBy94e9aO-807116467";"Лидия E")',
        '=HYPERLINK("https://app.tomoru.ru/bot/DMPfEuZ1TEPYDea26gBk/chats/jmSSJNV8wLWQvooCDxwQ-113378190";"Katerina Zhuravleva")',
        '=HYPERLINK("https://app.tomoru.ru/bot/DMPfEuZ1TEPYDea26gBk/chats/JoL3SuysP0fiBy94e9aO-175528246";"Evgenia Bystrova")',
        '=HYPERLINK("https://app.tomoru.ru/bot/DMPfEuZ1TEPYDea26gBk/chats/JoL3SuysP0fiBy94e9aO-867721476";"Виктория")',
        '=HYPERLINK("https://app.tomoru.ru/bot/DMPfEuZ1TEPYDea26gBk/chats/JoL3SuysP0fiBy94e9aO-430129191";"Denis Serezhin")',
        '=HYPERLINK("https://app.tomoru.ru/bot/DMPfEuZ1TEPYDea26gBk/chats/JoL3SuysP0fiBy94e9aO-979515307";"Рушания")',
        '=HYPERLINK("https://app.tomoru.ru/bot/DMPfEuZ1TEPYDea26gBk/chats/jmSSJNV8wLWQvooCDxwQ-35642923";"Марсель Гумер")',
        '=HYPERLINK("https://app.tomoru.ru/bot/DMPfEuZ1TEPYDea26gBk/chats/jmSSJNV8wLWQvooCDxwQ-391613276";"Martine La-Verne")',
        '=HYPERLINK("https://app.tomoru.ru/bot/DMPfEuZ1TEPYDea26gBk/chats/JoL3SuysP0fiBy94e9aO-797694863";"Ольга")',
        '=HYPERLINK("https://app.tomoru.ru/bot/DMPfEuZ1TEPYDea26gBk/chats/JoL3SuysP0fiBy94e9aO-778055782";"Денис Кораблев")',
        '=HYPERLINK("https://app.tomoru.ru/bot/DMPfEuZ1TEPYDea26gBk/chats/jmSSJNV8wLWQvooCDxwQ-108742628";"Диана Лукьянова")',
        '=HYPERLINK("https://app.tomoru.ru/bot/DMPfEuZ1TEPYDea26gBk/chats/JoL3SuysP0fiBy94e9aO-437488015";"khgrs")',
        '=HYPERLINK("https://app.tomoru.ru/bot/DMPfEuZ1TEPYDea26gBk/chats/JoL3SuysP0fiBy94e9aO-152614263";"Alina Slizova")',
        '=HYPERLINK("https://app.tomoru.ru/bot/DMPfEuZ1TEPYDea26gBk/chats/JoL3SuysP0fiBy94e9aO-436369380";"𝖄 / 𝕿")',
        '=HYPERLINK("https://app.tomoru.ru/bot/DMPfEuZ1TEPYDea26gBk/chats/JoL3SuysP0fiBy94e9aO-347682187";"Alex")',
        '=HYPERLINK("https://app.tomoru.ru/bot/DMPfEuZ1TEPYDea26gBk/chats/JoL3SuysP0fiBy94e9aO-502662503";"Гаянэ")',
        '=HYPERLINK("https://app.tomoru.ru/bot/DMPfEuZ1TEPYDea26gBk/chats/JoL3SuysP0fiBy94e9aO-147897633";"Алия Сафина")',
    ]

    assert extract_chats(values) == [
        "JoL3SuysP0fiBy94e9aO-678295990",
        "JoL3SuysP0fiBy94e9aO-304277490",
        "JoL3SuysP0fiBy94e9aO-826341750",
        "jmSSJNV8wLWQvooCDxwQ-159638777",
        "jmSSJNV8wLWQvooCDxwQ-185599130",
        "JoL3SuysP0fiBy94e9aO-845289386",
        "JoL3SuysP0fiBy94e9aO-544237010",
        "JoL3SuysP0fiBy94e9aO-304427935",
        "jmSSJNV8wLWQvooCDxwQ-3385555",
        "JoL3SuysP0fiBy94e9aO-807116467",
        "jmSSJNV8wLWQvooCDxwQ-113378190",
        "JoL3SuysP0fiBy94e9aO-175528246",
        "JoL3SuysP0fiBy94e9aO-867721476",
        "JoL3SuysP0fiBy94e9aO-430129191",
        "JoL3SuysP0fiBy94e9aO-979515307",
        "jmSSJNV8wLWQvooCDxwQ-35642923",
        "jmSSJNV8wLWQvooCDxwQ-391613276",
        "JoL3SuysP0fiBy94e9aO-797694863",
        "JoL3SuysP0fiBy94e9aO-778055782",
        "jmSSJNV8wLWQvooCDxwQ-108742628",
        "JoL3SuysP0fiBy94e9aO-437488015",
        "JoL3SuysP0fiBy94e9aO-152614263",
        "JoL3SuysP0fiBy94e9aO-436369380",
        "JoL3SuysP0fiBy94e9aO-347682187",
        "JoL3SuysP0fiBy94e9aO-502662503",
        "JoL3SuysP0fiBy94e9aO-147897633",
    ]
