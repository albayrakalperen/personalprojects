import requests
import os
from decouple import config
from twilio.rest import Client

OWM_Endpoint = "https://api.openweathermap.org/data/2.5/onecall"
api_key = config("api_key")
account_sid = config("account_sid")
auth_token = config("auth_token")
client = Client(account_sid, auth_token)

lat_lon_response = requests.get(url=f"http://api.openweathermap.org/geo/1.0/direct?q=Antalya&limit=5&appid={api_key}")
lat_lon_response.raise_for_status()
MY_LATITUDE = lat_lon_response.json()[0]["lat"]
MY_LONGITUDE = lat_lon_response.json()[0]["lon"]

weather_params = {
    "lat": MY_LATITUDE,
    "lon": MY_LONGITUDE,
    "appid": api_key,
    "exclude": "current,minutely,daily"
}

weather_response = requests.get(OWM_Endpoint, params=weather_params)
weather_response.raise_for_status()
weather_data = weather_response.json()
weather_slice = weather_response.json()["hourly"][:12]
print(weather_data)

will_rain = False

for hour_data in weather_slice:
    condition_code = hour_data["weather"][0]["id"]
    if int(condition_code) < 700:
        will_rain = True

if will_rain:
    message = client.messages.create(
        from_='whatsapp:+14155238886',
        body='Bugün hava yağışlı.',
        to=f'whatsapp:{config("whatsapp_number")}'
    )

else:
    message = client.messages.create(
        from_='whatsapp:+14155238886',
        body='Bugün hava yağışlı değil.',
        to=f'whatsapp:{config("whatsapp_number")}'
    )
