from core_app import Scrapper
from web import Web_display

import datetime

url = 'https://www.otomoto.pl/osobowe/audi/a6'
csv_name = url[31:].replace('/', '-') + '-' + str(datetime.date.today())

if __name__ == '__main__':

    app = Scrapper()

    app.scrap_to_csv(url, csv_name)
    #app.from_csv_to_db(csv_name)



''' wd = Web_display(app.conn)
    wd.app.run(debug=False, host='192.168.0.23', port=4999)'''

