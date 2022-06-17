import requests
import smtplib
from decouple import config

MY_MAIL = config("MY_MAIL")
MY_PW = config("MY_PW")
USERS_ENDPOINT = "https://api.sheety.co/************/flightDeals/users"
PRICES_ENDPOINT = "https://api.sheety.co/***********/flightDeals/prices"


class UserMailManager:

    def ask_questions(self):
        user_info = {"first_name": None, "last_name": None, "email": None}
        print("Welcome to flight club.\nWe find the best flight deals for you.")
        ask_first_name = input("What is your first name?\n")
        ask_last_name = input("What is your last name?\n")
        ask_email = input("What is your e-mail?\n")
        ask_verification = input("Please enter your e-mail again.\n")

        if ask_email == ask_verification:
            print("You are in the club!")
            user_info["first_name"] = ask_first_name
            user_info["last_name"] = ask_last_name
            user_info["email"] = ask_email

        else:
            print("E-mails does not match. Please try again.")

        return user_info

    def read_prices(self):
        response = requests.get(url=PRICES_ENDPOINT)
        return response.json()["prices"]

    def read_users(self):
        response = requests.get(url=USERS_ENDPOINT)
        return response.json()["users"]

    def write_user(self, ask_questions):

        headers = {
            "Content-Type": "application/json"
        }
        json = {
            "user": {
                "firstName": ask_questions["first_name"],
                "lastName": ask_questions["last_name"],
                "eMail": ask_questions["email"],
                "id": 2
            }
        }
        response = requests.post(url=USERS_ENDPOINT, json=json, headers=headers)

    def send_mail(self, target_mail, message):
        with smtplib.SMTP("smtp.ethereal.email", port=587) as connection:
            connection.starttls()
            connection.login(user=MY_MAIL, password=MY_PW)
            connection.sendmail(from_addr=MY_MAIL,
                                to_addrs=target_mail,
                                msg=message)

