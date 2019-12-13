from flask import Flask, request, redirect, url_for, render_template
import sqlite3
from urlparse import urlparse
from sqlite3 import Error
from flask_bootstrap import Bootstrap
from datetime import datetime

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
        if('update' in request.form):
            genus = request.form.get('genus')
            species = request.form.get('species')

            if(genus == ''):
                genus = latin_name[0][0]
            if(species == ''):
                species = latin_name[0][1]

            update_db(connection, "UPDATE flowers SET genus=?, species=? WHERE comname=?", (genus, species, f,))
        
        elif('insert' in request.form):
            sighted = datetime.strptime(request.form.get('sighted'), '%Y-%m-%d')
            insert_db(connection, "INSERT INTO sightings(name, person, location, sighted) VALUES(?,?,?,?)", (f, request.form.get('person'), request.form.get('location'), sighted.date(),))
        
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
    
    print("New Genus: " + vars[0] + "\nNew Species: " + vars[1])
    cursor.execute(update, vars)
    
    connection.commit()

def insert_db(connection, insert, vars):
    cursor = connection.cursor()
    
    print("New sighting of " + vars[0] + " by " + vars[1] + " at " + vars[2] + " on " + datetime.strftime(vars[3], '%Y-%m-%d') + ".")
    cursor.execute(insert, vars)
    connection.commit()
    return cursor.lastrowid

if __name__ == '__main__':
    app.run(debug=True, port=5000)