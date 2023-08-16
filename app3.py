from bs4 import BeautifulSoup
import requests
import csv

url = 'https://www.otomoto.pl/osobowe/land-rover/defender/od-1998?search%5Bfilter_float_year%3Ato%5D=2015'
page = requests.get(url)
print(page.status_code)

soup = BeautifulSoup(page.content, 'html.parser')
# soup

lists = soup.find_all('article', class_='ooa-1rudse5')

with open('cars.csv', 'w', encoding='utf8', newline='') as f:
    thewriter =csv.writer(f)
    header = ['Title', 'Price', 'Year_of_production']
    thewriter.writerow(header)
    for list in lists:
        title = list.find('a', href = True).string
        price = list.find('span', class_='ooa-1bmnxg7').string
        year = list.find('li', class_='ooa-1k7nwcr e19ivbs0').string
        # mileage = list.find('li', class_='ooa-1k7nwcr e19ivbs0').string
        info = [title, price, year]
        thewriter.writerow(info)
        # print(info)