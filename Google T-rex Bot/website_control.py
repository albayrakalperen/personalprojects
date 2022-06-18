from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

DRIVER_PATH = "C:\Development\chromedriver.exe"
WEBSITE_LINK = "https://elgoog.im/t-rex/"


class Trex:

    def __init__(self):
        self.service = Service(DRIVER_PATH)
        self.driver = webdriver.Chrome(executable_path=DRIVER_PATH)
        self.driver.get(WEBSITE_LINK)
        self.driver.maximize_window()
        self.canvas = self.driver.find_element(By.XPATH, '/html/body/header/p[3]')
        self.canvas.click()
