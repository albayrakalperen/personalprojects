from decouple import config
from twilio.rest import Client

ACCOUNT_SID = config("ACCOUNT_SID")
AUTH_TOKEN = config("AUTH_TOKEN")
TWILIO_NUMBER = config("TWILIO_NUMBER")

class NotificationManager:

    def __init__(self):
        self.client = Client(ACCOUNT_SID, AUTH_TOKEN)

    def send_sms(self, message):
        self.client.messages.create(
            from_=f"whatsapp:{TWILIO_NUMBER}",
            body=message,
            to=f'whatsapp:{config("WHATSAPP_NUMBER")}'
        )
