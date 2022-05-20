import gspread
import requests
import openpyxl
from io import BytesIO

gc = gspread.service_account()
print(gspread.auth)
at = gc.auth.token
at = gspread.auth
print(at)
url = "https://www.googleapis.com/drive/v3/files/1KB_prFcbjUlfCTZpQCBVVk8Cqabp6Gb3NFbi53WoP8o/export?mimeType=application%2Fvnd.openxmlformats-officedocument.spreadsheetml.sheet"

res = requests.get(url, headers={"Authorization": "Bearer" + at})

book = openpyxl.load_workbook(filename=BytesIO(res.content), data_only=False)
hd_sheet = book.active
#sh = gc.open("Disgaea RPG Translations of Characters")

print(hd_sheet.get('A1'))