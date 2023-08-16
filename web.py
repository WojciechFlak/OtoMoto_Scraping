from flask import Flask, render_template, request, redirect, url_for
from flask.views import View
import sqlite3
import csv

app = Flask(__name__)

class Web_display:

    def __init__(self, db_conn):
        self.conn = db_conn
        self.app = Flask(__name__)

    def get_items(self):
        items = self.conn.execute('SELECT * FROM items').fetchall()
        return items


    # Routes
    @app.route('/')
    def index(self):
        items = self.conn.execute('SELECT * FROM items').fetchall()
        self.conn.close()
        return render_template('index.html', items=items)

'''
    @app.route('/add', methods=['POST'])
    def add_item():
        item_name = request.form['item_name']
        conn = get_db_connection()
        conn.execute('INSERT INTO items (name) VALUES (?)', (item_name,))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))


    @app.route('/edit/<int:id>', methods=['GET', 'POST'])
    def edit_item(id):
        conn = get_db_connection()
        item = conn.execute('SELECT * FROM items WHERE id = ?', (id,)).fetchone()

        if request.method == 'POST':
            new_name = request.form['item_name']
            conn.execute('UPDATE items SET name = ? WHERE id = ?', (new_name, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

        conn.close()
        return render_template('edit.html', item=item)


    @app.route('/delete/<int:id>', methods=['POST'])
    def delete_item(id):
        conn = get_db_connection()
        conn.execute('DELETE FROM items WHERE id = ?', (id,))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))


    @app.route('/generate_csv')
    def generate_csv():
        items = get_items()
    
        # Create a CSV string
        csv_data = "\n".join([item[1] for item in items])
    
        response = app.response_class(
            csv_data,
            mimetype='text/csv',
            headers={'Content-Disposition': 'attachment; filename=items.csv'}
             )
        return response
'''
if __name__ == '__main__':

    app.run(debug=False, host='192.168.0.23', port=4999)


