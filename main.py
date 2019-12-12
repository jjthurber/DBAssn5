from flask import Flask, request, redirect, url_for, render_template
import sqlite3
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
def flower_page(f):
    connection = new_connection(_db_name_)
    sightings = enumerate(query_db(connection, "SELECT * FROM sightings WHERE name=? ORDER BY datetime(sighted) DESC LIMIT 10", (f,)))
    print(f)
    return render_template('flower.html', f=f, sightings=sightings)

def query_db(connection, query, var):
    cursor = connection.cursor()
    if var == None:
        cursor.execute(query)
    else:
        cursor.execute(query, var)
    return cursor.fetchall()

# def update_db(connection, update):


# def insert_db(connection, insert):
    

def all_flowers_by_comname(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM flowers ORDER BY comname")
    
    return cursor.fetchall()

def select_flower_by_comname(connection, comname):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM flowers WHERE comname=? ORDER BY comname", (comname,))
    
    return cursor.fetchall()

def all_sightings_by_flower(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM sightings ORDER BY name")
    
    return cursor.fetchall()

def select_sighting_by_flower(connection, flower):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM sightings WHERE name=? ORDER BY sighted", (flower,))
    
    return cursor.fetchall()

# def main():
    
#     connection = new_connection(database)

#     app.run()

#     print("Full list of sightings:")
#     all_sightings_by_flower(connection)

#     print("Selecting sightings for only 'Butter and eggs'")
#     select_sighting_by_flower(connection, "Butter and eggs")

if __name__ == '__main__':
    app.run(debug=True, port=5000)