import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

DRIVER_PATH = "C:\Development\chromedriver.exe"
WEBSITE_LINK = "WEBSITE"


class SteamDB:

    def __init__(self):
        self.service = Service(DRIVER_PATH)
        self.driver = webdriver.Chrome(executable_path=DRIVER_PATH)
        self.driver.get(WEBSITE_LINK)

    def get_game_list(self):
        app_list = []
        apps = self.driver.find_elements(By.CLASS_NAME, "app")

        for app in apps:
            app_list.append(app.text.split())

        self.driver.quit()
        return app_list

    @staticmethod
    def create_csv(app_list):
        header = ["game_id", "game_name", "current_player", "peak_24h", "all_time_peak"]

        with open("website_data.csv", "w", encoding="UTF8", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(header)
            for app in app_list:
                game_id = int(app[0].replace(".", ""))
                game_name = " ".join(app[1:-4])
                current_player = int(app[-4].replace(",", ""))
                peak_24h = int(app[-3].replace(",", ""))
                all_time_peak = int(app[-2].replace(",", ""))
                writer.writerow([game_id, game_name, current_player, peak_24h, all_time_peak])
                
