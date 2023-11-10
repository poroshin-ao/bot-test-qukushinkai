import sqlite3
from internal.models.SQLite_db.db_connect import *
from internal.models.SQLite_db.set_category import set_category

def set_turnir(data, data_file, destination):
    connection, cursor = open_connect()

    tur_exec = "INSERT INTO TURNIRS(name, place, date, file_name) VALUES (@0, @1, @2, @3)"
    cursor.execute(tur_exec, [data["tur_name"], data["tur_place"], data["tur_date"], destination])

    close_connect(connection)

    for cat, members in data_file.items():
        set_category(data["tur_name"], data["tur_date"], cat, members)
    