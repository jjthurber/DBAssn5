import flask
import sqlite3
from sqlite3 import Error

#Sources used:
#https://www.sqlitetutorial.net/sqlite-python/sqlite-python-select/

def new_connection(dbName):
    newConnection = None

    try:
        newConnection = sqlite3.connect(dbName)
        print("DB Connected!")
    except Error as e:
        print(e)

    return newConnection

def all_flowers_by_comname(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM flowers ORDER BY comname")
    
    rows = cursor.fetchall()

    for row in rows:
        print(row)

def select_flower_by_comname(connection, comname):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM flowers WHERE comname=? ORDER BY comname", (comname,))
    
    rows = cursor.fetchall()

    for row in rows:
        print(row)

def all_sightings_by_flower(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM sightings ORDER BY name")
    
    rows = cursor.fetchall()

    for row in rows:
        print(row)

def select_sighting_by_flower(connection, flower):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM sightings WHERE name=? ORDER BY sighted", (flower,))
    
    rows = cursor.fetchall()

    for row in rows:
        print(row)

def main():
    database = "flowers2019.db"
    connection = new_connection(database)

    print("Full list of sightings:")
    all_sightings_by_flower(connection)

    print("Selecting sightings for only 'Butter and eggs'")
    select_sighting_by_flower(connection, "Butter and eggs")

if __name__ == '__main__':
    main()