import time
import speedtest
from decouple import config
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException

PROMISED_DOWNLOAD = 100
PROMISED_UPLOAD = 8
CHROME_PATH = "C:\Development\chromedriver.exe"
EMAIL = config("EMAIL")
PASSWORD = config("PASSWORD")

driver = webdriver.Chrome(service=service)
driver.get("SOCIAL MEDIA PLATFORM")
time.sleep(3)


class SpeedComplaintBot:
    def __init__(self):
        self.servers = []
        self.threads = None
        self.dl = 0
        self.ul = 0

    def perform_speed_test(self):
        self.s = speedtest.Speedtest()
        self.s.get_servers(servers=self.servers)
        self.s.get_best_server()
        self.s.download(threads=self.threads)
        self.s.upload(threads=self.threads)
        results = self.s.results.dict()
        print(results)
        dl_unrounded = results["download"]/1000000
        dl_rounded = round(dl_unrounded, 2)
        self.dl = dl_rounded
        print(dl_rounded)
        ul_unrounded = results["upload"] / 1000000
        ul_rounded = round(ul_unrounded, 2)
        self.ul = ul_rounded
        print(ul_rounded)

    def share_with_social_media_platform(self, driver_path):
        self.service = Service(driver_path)
        self.driver = webdriver.Chrome(service=self.service)
        self.driver.get("SOCIAL MEDIA PLATFORM")
        time.sleep(2)

        enter_email = self.driver.find_element(By.ID, "email")
        enter_email.send_keys(EMAIL)
        enter_password = self.driver.find_element(By.ID, "pass")
        enter_password.send_keys(PASSWORD)
        enter_password.send_keys(Keys.RETURN)
        time.sleep(5)

        plus_button = self.driver.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/div[2]/div[3]/div/div[1]/div[1]/ul/li[1]/span/div/a")
        plus_button.click()
        time.sleep(2)

        what_do_you_think = self.driver.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div[2]/div/div/div/div[3]/div/div[2]/div/div/div/div[1]/div/div[1]/span")
        what_do_you_think.click()
        time.sleep(2)

        writable_space = self.driver.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/form/div/div[1]/div/div/div/div[2]/div[1]/div[1]/div[1]/div/div/div/div/div/div/div[2]/div/div/div/div")
        writable_space.send_keys("Here is my internet speed test results:\n"
                                 f"{self.dl} Mbps download / {self.ul} Mbps upload\n"
                                 f"You promised me {PROMISED_DOWNLOAD} Mbps download / {PROMISED_UPLOAD} Mbps upload!")
        time.sleep(2)

        share_button = self.driver.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/form/div/div[1]/div/div/div/div[3]/div[2]/div/div/div[1]/div/span/span")
        share_button.click()


bot = SpeedComplaintBot()
bot.perform_speed_test()
bot.share_with_social_media_platform(CHROME_PATH)


