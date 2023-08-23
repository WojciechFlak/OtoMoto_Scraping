import sqlite3
import pandas
from bs4 import BeautifulSoup
import requests
import time
import re

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

    def count_pages(self, url):

        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        pagination_div = soup.find("ul", class_="pagination-list")
        max_page = 1
        if pagination_div:
            # Find all links within the pagination element
            pagination_links = pagination_div.find_all("a")

            max_page = 0
            try:
                for link in pagination_links:
                    page_number = int(link.text)
                    max_page = max(max_page, page_number)
            except ValueError:
                max_page = 1
        return max_page



    def scrap_to_csv(self, url, csv_file):
        self.url = url
        self.csv_file = csv_file

        page_number = self.count_pages(self.url)
        print(f"Total number of pages: {page_number}")
        if page_number == 1:
            page_number = 2

        for i in range(1, page_number):
            url = self.url + '?page=' + str(i)

            page = requests.get(url)

            soup = BeautifulSoup(page.content, 'html.parser')

            lists = soup.find_all('article', class_='ooa-1t80gpj ev7e6t818')
            # lists2 = soup.find_all('article', class_='ooa-j8iifw evg565y0')
            # lists3 = soup.find_all('article', class_='ooa-13ci8fj evg565y0')  # wyróżnione
            #lists4 = soup.find_all('article', class_="ooa-1t80gpj ev7e6t818")  # wyróżnione

            # lists += lists2
            # lists += lists3
            #lists +=lists4

            #time.sleep(2)

            with open(self.csv_file, 'a', encoding='utf8', newline='') as f:
                thewriter = csv.writer(f)
                if i == 1:
                    header = ['Title', 'Price', 'Currency', 'Year_of_production', 'Mileage', 'Engine_type', 'Engine', 'update_tmstmp']
                    thewriter.writerow(header)
                for list in lists:
                    title = list.find('h1').string
                    price = list.find('h3', class_='ev7e6t82 ooa-bz4efo er34gjf0').string
                    currency = list.find('p', class_='ev7e6t81 ooa-1e3jyoe er34gjf0').string
                    year = list.find('dd', {'data-parameter': 'year'})
                    mileage = list.find('dd', {'data-parameter': 'mileage'})
                    engine_type = list.find('dd', {'data-parameter': 'fuel_type'})

                    # In case in larger boxes this data is provided within ""
                    try:
                        engine = re.split("•", list.find('p').string)
                    except:
                        engine =re. split("•", list.find('p', class_="ev7e6t88 ooa-17thc3y er34gjf0").string)

                    update_tmstmp = datetime.datetime.now().strftime("%d-%m-%Y, %H:%M")

                    price = price.replace(' ', '')
                    currency = currency.replace(' ', '')
                    year = year.get_text(strip=True)

                    # In case there is no mileage provided on the website (new car from dealer)
                    try:
                        mileage = mileage.get_text(strip=True).replace(' ', '').replace('km', '')
                    except:
                        mileage = 0
                    engine_type = engine_type.get_text(strip=True)

                    engine = engine[0].strip()


                    info = [title,
                            price,
                            currency,
                            year,
                            mileage,
                            engine_type,
                            engine,
                            update_tmstmp]
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








