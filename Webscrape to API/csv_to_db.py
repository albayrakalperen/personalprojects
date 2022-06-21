import csv
import sqlite3
from webscraping_steamdb import SteamDB


class CSVtoDB:

    def __init__(self):
        self.steam_db = SteamDB()
        self.games = self.steam_db.get_game_list()
        self.steam_db.create_csv(self.games)

    @staticmethod
    def create_database():
        con = sqlite3.connect('website.db')
        print(type(con))
        cur = con.cursor()

        try:
            cur.execute('CREATE TABLE steam (game_id, game_name, current_player, peak_24h, all_time_peak);')

        except sqlite3.OperationalError:
            cur.execute('DROP TABLE steam;')
            cur.execute('CREATE TABLE steam (game_id, game_name, current_player, peak_24h, all_time_peak);')

        finally:
            with open("steam_db.csv", "r") as csv_file:
                dr = csv.DictReader(csv_file)
                to_db = [(i["game_id"], i["game_name"], i["current_player"], i["peak_24h"], i["all_time_peak"]) for i in dr]

            cur.executemany('INSERT INTO steam (game_id, game_name, current_player, peak_24h, all_time_peak) VALUES (?, ?, ?, ?, ?);', to_db)
            con.commit()
            con.close()
            
