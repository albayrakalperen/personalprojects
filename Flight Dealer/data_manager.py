import requests

SHEETY_ENDPOINT = "https://api.sheety.co/******/flightDeals/prices"

#This class is responsible for talking to the Google Sheet.
class DataManager:
    def get_city_name(self):
        response = requests.get(url=SHEETY_ENDPOINT)
        response.raise_for_status()
        return response.json()["prices"]

    def update_iata_code(self, code, id):
        edit_url = f"{SHEETY_ENDPOINT}/{id}"
        params = {
            "price": {
                "iataCode": code
            }
        }
        response = requests.put(url=edit_url, json=params)


    def update_price(self, price, id):
        edit_url = f"{SHEETY_ENDPOINT}/{id}"
        params = {
            "price": {
                "lowestPrice": price
            }
        }
        response = requests.put(url=edit_url, json=params)
        print(response.text)


