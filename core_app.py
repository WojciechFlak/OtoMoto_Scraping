import sqlite3
import pandas
from bs4 import BeautifulSoup
import requests

import csv
import datetime


class Scrapper:

    def __init__(self):
        self.conn = sqlite3.connect('car_records.db')
        self.create_table()

    def create_table(self):
        self.conn.execute(
            '''
            CREATE TABLE IF NOT EXISTS cars (
                id INTEGER PRIMARY KEY,
                title TEXT,
                price TEXT,
                year_of_production INTEGER,
                milage,
                engine,
                update_tmstmp TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
            )
        '''
        )
        self.conn.commit()

    def scrap_to_csv(self, url, csv_file):
        self.url = url
        self.csv_file = csv_file
        for i in range(1, 6):
            url = self.url + '?page=' + str(i)

            page = requests.get(url)

            soup = BeautifulSoup(page.content, 'html.parser')

            lists = soup.find_all('article', class_='ooa-2wq0y evg565y0')
            lists2 = soup.find_all('article', class_='ooa-j8iifw evg565y0')
            lists3 = soup.find_all('article', class_='ooa-13ci8fj evg565y0')  # wyróżnione

            lists += lists2
            lists += lists3

            with open(self.csv_file, 'a', encoding='utf8', newline='') as f:
                thewriter = csv.writer(f)
                if i == 1:
                    header = ['Title', 'Price', 'Year_of_production', 'Milage', 'Engine', 'update_tmstmp']
                    thewriter.writerow(header)
                for list in lists:
                    title = list.find('a', href=True).string
                    price = list.find('span', class_='ooa-1bmnxg7').string
                    year = list.select('li', class_='ooa-1k7nwcr euadd4q0')[0].string
                    milage = list.select('li', class_='ooa-1k7nwcr euadd4q0')[1].string
                    engine = list.select('li', class_='ooa-1k7nwcr euadd4q0')[2].string
                    update_tmstmp = datetime.datetime.now().strftime("%d-%m-%Y, %H:%M")
                    info = [title, price[:-4].replace(' ', ''), year, milage[:-3].replace(' ', ''), engine, update_tmstmp]
                    thewriter.writerow(info)

    def from_csv_to_db(self, csv_file):
        with open(csv_file, 'r') as csvfile:
            datareader = csv.reader(csvfile)
            for row in datareader:
                if 'Title' in row:
                    pass
                else:
                    title = row[0]
                    price = row[1]
                    year = row[2]
                    milage = row[3]
                    engine = row[4]

                    # Insert the data into the database
                    self.conn.execute('INSERT INTO cars (title, price, year_of_production, milage, engine) VALUES (?, ?, ?, ?, ?)',(title, price, year, milage, engine))
                    # Commit the changes and close the database connection
        self.conn.commit()





