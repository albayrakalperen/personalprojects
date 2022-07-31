import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service

CHROME_PATH = "C:\Development\chromedriver.exe"
RENTAL_WEBSITE_URL = "URL"
GOOGLE_FORM_URL = "URL"


class RentalFinder:

    def __init__(self):
        self.service = Service(CHROME_PATH)
        self.driver = webdriver.Chrome(service=self.service)
        self.driver.get(ZILLOW_URL)
        self.all_addresses_list = []
        self.all_prices_list = []
        self.all_links_list = []

    def get_info(self, ):
        all_addresses = self.driver.find_elements(By.CLASS_NAME, "list-card-addr")
        self.all_addresses_list = [address.text for address in all_addresses]
        print(self.all_addresses_list)
        print(len(self.all_addresses_list))

        all_prices = self.driver.find_elements(By.CLASS_NAME, "list-card-price")
        self.all_prices_list = [price.text.split()[0].replace("+", "").replace("/mo", "").replace(",", "") for price in all_prices]
        print(self.all_prices_list)
        print(len(self.all_prices_list))

        all_links = self.driver.find_elements(By.CSS_SELECTOR, ".list-card-info a")
        self.all_links_list = [link.get_attribute("href") for link in all_links]
        print(self.all_links_list)
        print(len(self.all_links_list))

    def create_lists(self):
        # list_container = self.driver.find_element(By.CSS_SELECTOR, ".search-page-container map-on-left div")
        #
        # vertical_ordinate = 100
        # for _ in range(10):
        #     print(vertical_ordinate)
        #     self.driver.execute_script("arguments[0].scrollTop = arguments[1]", list_container, vertical_ordinate)
        #     vertical_ordinate += 100
        #     # time.sleep(1)

        page = self.driver.find_element(By.TAG_NAME, "html")
        for _ in range(10):
            self.get_info()
            time.sleep(2)
            page.send_keys(Keys.PAGE_DOWN)
        time.sleep(5)

    def fill_form(self):
        self.driver.get(GOOGLE_FORM_URL)
        time.sleep(5)
        for i in range(len(self.all_addresses_list)):

            address_input = self.driver.find_element(By.XPATH, "//*[@id='mG61Hd']/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input")
            price_input = self.driver.find_element(By.XPATH, "//*[@id='mG61Hd']/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input")
            link_input = self.driver.find_element(By.XPATH, "//*[@id='mG61Hd']/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input")
            send_button = self.driver.find_element(By.XPATH, "/html/body/div/div[2]/form/div[2]/div/div[3]/div[1]/div[1]/div/span/span")

            address_input.send_keys(self.all_addresses_list[i])
            price_input.send_keys(self.all_prices_list[i])
            link_input.send_keys(self.all_links_list[i])
            send_button.click()
            time.sleep(3)
            send_another_button = self.driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[1]/div/div[4]/a")
            send_another_button.click()
            time.sleep(3)


rental_findings = RentalFinder()
rental_findings.create_lists()
rental_findings.fill_form()

