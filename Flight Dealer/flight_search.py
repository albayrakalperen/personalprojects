import requests
import os
from flight_data import FlightData
from decouple import config

TEQUILA_ENDPOINT = "https://tequila-api.kiwi.com"
API_KEY = config('API_KEY')

class FlightSearch:
    #This class is responsible for talking to the Flight Search API.

    def get_iata_code(self, city_name):
        locations_url = f"{TEQUILA_ENDPOINT}/locations/query"
        headers= {
            "apikey": API_KEY,
            "Content-Encoding": "gzip"
        }
        params = {
            "term": city_name,
            "location_types": "city"

        }
        response = requests.get(url=locations_url, params=params, headers=headers)
        code = response.json()["locations"][0]["code"]
        return code

    def get_flight_data(self, fly_from, fly_to, date_from, date_to):
        flight_data_url = f"{TEQUILA_ENDPOINT}/v2/search"
        headers = {
            "apikey": API_KEY,
            "Content-Encoding": "gzip",
            "Content-Type": "json"
        }
        params = {
            "fly_from": fly_from,
            "fly_to": fly_to,
            "date_from": date_from,
            "date_to": date_to,
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 10,
            "one_for_city": 1,
            "flight_type": "round",
            "max_stopovers": 0,
            "curr": "GBP"
        }
        response = requests.get(url=flight_data_url, params=params, headers=headers)
        
        try:
            price = response.json()["data"][0]["price"]
            from_airport = response.json()["data"][0]["route"][0]["flyFrom"]
            to_airport = response.json()["data"][0]["route"][0]["flyTo"]

            arrival = response.json()["data"][0]["route"][0]["local_arrival"]
            arrival_date = arrival.split("T")[0]
            arrival_time = arrival.split("T")[1].split(".")[0]

            departure = response.json()["data"][0]["route"][0]["local_departure"]
            departure_date = departure.split("T")[0]
            departure_time = departure.split("T")[1].split(".")[0]

            flight_data = FlightData(
                price,
                from_airport,
                to_airport,
                arrival_date,
                arrival_time,
                departure_date,
                departure_time
            )

            return flight_data

        except:
            print(f"No flights for {fly_to}.")
            return None
