from decouple import config
from bs4 import BeautifulSoup
import requests
import smtplib

TARGET_PRICE = 200
PRODUCT_URL = "PRODUCT_URL"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/100.0.4896.127 Safari/537.36 OPR/86.0.4363.50",
    "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7"
}

response = requests.get(url=PRODUCT_URL, headers=headers)
amazon_ram_page = response.text
soup = BeautifulSoup(amazon_ram_page, "html.parser")
price = soup.find(name="span", class_="a-offscreen")
float_price = float(price.getText().split("$")[1])

my_email = config("my_email")
password = config("password")
if float_price < TARGET_PRICE:
    with smtplib.SMTP("smtp.ethereal.email", port=587) as connection:
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(
            from_addr=my_email,
            to_addrs=config("to_addrs"),
            msg=f"Subject: Low Price Alert!\n\nThe product is now ${float_price}!"
        )
