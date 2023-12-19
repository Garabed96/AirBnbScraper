import gspread
from oauth2client.service_account import ServiceAccountCredentials

# gspread documentation: https://docs.gspread.org/en/latest/

scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]


def upload_csv_to_sheets():
    credentials = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(credentials)

    spreadsheet = client.open('Airbnb saved rental list')

    with open('airbnb_rentals.csv', 'r') as file_obj:
        content = file_obj.read()
        client.import_csv(spreadsheet.id, data=content)