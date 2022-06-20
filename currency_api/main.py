import csv
import requests
from decouple import config

API_KEY = config("API_KEY")
BASE_URL = "https://api.apilayer.com/exchangerates_data/timeseries?start_date=2021-01-01&end_date=2021-01-10"
payload = {}
headers = {
  "apikey": API_KEY
}
response = requests.request("GET", BASE_URL, headers=headers, data=payload)
status_code = response.status_code
result = response.json()

csv_header = ["date", "name", "value"]
with open("currency.csv", "w", encoding="UTF8", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(csv_header)

    for date in result["rates"]:
        for name, value in result["rates"][date].items():
            writer.writerow([date, name, value])
