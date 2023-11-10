import sqlite3

def open_connect():
    connection = sqlite3.connect(".\storage\data_base\database.db")
    cursor = connection.cursor()
    return connection, cursor

def close_connect(connection):
    connection.commit()
    connection.close()
