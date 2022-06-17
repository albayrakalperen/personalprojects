from datetime import datetime, timedelta
from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager
from user_mail_manager import UserMailManager

data_manager = DataManager()
flight_search = FlightSearch()
user_mail_manager = UserMailManager()
notification_manager = NotificationManager()
sheet_data = data_manager.get_city_name()

for row in sheet_data:
    if row["lowestPrice"] == "":
        code = flight_search.get_iata_code(row["city"])
        print(code)
        write = data_manager.update_iata_code(code=code, id=row["id"])

ORIGIN_CITY = "LON"

tomorrow = datetime.date(datetime.now() + timedelta(days=1)).strftime("%d/%m/%Y")
six_months_from_tomorrow = datetime.date(datetime.now() + timedelta(days=180)).strftime("%d/%m/%Y")

for row in sheet_data:
    flight = flight_search.get_flight_data(fly_from=ORIGIN_CITY,
                                  fly_to=row["iataCode"],
                                  date_from=tomorrow,
                                  date_to=six_months_from_tomorrow)


    if not flight == None and row["lowestPrice"] > flight.price:
        message = f"Low price alert! {flight.from_airport} - {flight.to_airport} " \
                  f"{flight.price}£! Departure: {flight.departure_date}, {flight.departure_time} " \
                  f"Arrival: {flight.arrival_date}, {flight.arrival_time}".encode('utf-8')

        x = data_manager.update_price(flight.price, row["id"])
        print(flight.price)
        notification_manager.send_sms(message)
        for user in user_mail_manager.read_users():
            user_mail_manager.send_mail(user["eMail"], message)
