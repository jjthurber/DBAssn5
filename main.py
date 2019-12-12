from flask import Flask, request, redirect, url_for, render_template
import sqlite3
from urlparse import urlparse
from sqlite3 import Error
from flask_bootstrap import Bootstrap

#Sources used:
#https://www.sqlitetutorial.net/sqlite-python/sqlite-python-select/

_db_name_ = "flowers2019.db"

app = Flask(__name__)
bootstrap = Bootstrap(app)

def new_connection(db_name):
    connection = None
    try:
        connection = sqlite3.connect(db_name)
    except Error as e:
        print(e)
 
    return connection

@app.route('/', methods = ['GET', 'POST'])
def home_page():
    connection = new_connection(_db_name_)
    flowers = enumerate(query_db(connection, "SELECT * FROM flowers ORDER BY comname", None))
    return render_template('home.html', flowers=flowers)

@app.route('/flower/<f>', methods = ['GET', 'POST']) #Work in progress
def get_flower_page(f):
    connection = new_connection(_db_name_)
    sightings = enumerate(query_db(connection, "SELECT * FROM sightings WHERE name=? ORDER BY datetime(sighted) DESC LIMIT 10", (f,)))
    latin_name = query_db(connection, "SELECT genus, species FROM flowers WHERE comname=?", (f,))
    
    if(request.method == 'POST'):
        update_db(connection, "UPDATE flowers SET genus=?, species=? WHERE comname=?", (request.form.get('genus'), request.form.get('species'), f,))
        return redirect(request.url)
    return render_template('flower.html', f=f, genus=latin_name[0][0], species=latin_name[0][1], sightings=sightings)


def query_db(connection, query, var):
    cursor = connection.cursor()
    if var == None:
        cursor.execute(query)
    else:
        cursor.execute(query, var)
    return cursor.fetchall()

def update_db(connection, update, vars):
    cursor = connection.cursor()
    cursor.execute(update, vars)
    connection.commit()

# def insert_db(connection, insert):

if __name__ == '__main__':
    app.run(debug=True, port=5000)