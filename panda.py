import pandas
import sqlite3
import matplotlib.pyplot as plt


conn = sqlite3.connect('car_records.db')

data = pandas.read_sql_query("SELECT * FROM cars", conn)
data = data.drop(axis=1, labels=['id', 'title', 'update_tmstmp'])

data = data[data.year_of_production != 'Niski przebieg']
data = data[data.year_of_production < 2017]


data = data.astype({'price': 'int'})

fig, ax = plt.subplots()
ax.plot(data['year_of_production'], data['price'], 'bo')
plt.show()


