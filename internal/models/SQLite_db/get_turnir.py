import sqlite3
from internal.models.SQLite_db.db_connect import *


def get_tur_data_by_id(id):
    exec = "SELECT name, place, date FROM TURNIRS WHERE id = @0"

    connection, cursor = open_connect()
    
    cursor.execute(exec, [id])
    data = cursor.fetchone()

    close_connect(connection)

    return data


def get_turnir_name_place_date():
    exec = "SELECT name, place, date, id FROM TURNIRS"

    connection, cursor = open_connect()

    cursor.execute(exec)
    rows = cursor.fetchall()
    
    close_connect(connection)

    return rows


def get_fullturnir_by_name_date(name, date):
    exec = "SELECT TURNIRS.id, TURNIRS.name, CATEGORIES.id, CATEGORIES.category, MEMBERS.id, MEMBERS.fio, MEMBERS.n_fights, MEMBERS.n_wons \
            FROM TURNIRS JOIN CATEGORIES ON TURNIRS.id=CATEGORIES.t_id JOIN MEMBERS ON CATEGORIES.id=MEMBERS.c_id \
            WHERE TURNIRS.name = @0 AND TURNIRS.date = @1"

    connection, cursor = open_connect()

    cursor.execute(exec, [name, date])
    rows = cursor.fetchall()

    close_connect(connection)
    
    if len(rows) != 0:
        return fullturnir_row_to_dict(rows)
    else:
        return rows

def fullturnir_row_to_dict(row):
    tur_id = row[0][0]
    tur_name = row[0][1]

    d = dict()
    d[(tur_id, tur_name)] = dict()

    unic = unicum_cat(row)
    for i in unic:
        d[(tur_id, tur_name)][(i[0],i[1])] = []

    for i in row:
        d[(i[0],i[1])][(i[2],i[3])].append({"id":i[4],"fio":i[5],"n_fights":i[6],"n_wons":i[7]})

    return d

def unicum_cat(row):
    unic = []
    for i in row:
        if [i[2],i[3]] not in unic:
            unic.append([i[2],i[3]])

    return unic   

def get_turid_catid_stage(id):
    exec = "SELECT t.id, c.id, c.state FROM TURNIRS AS t JOIN CATEGORIES AS c ON t.id = c.t_id WHERE t.id = @0"

    connection, cursor = open_connect()

    cursor.execute(exec, [id])
    data = cursor.fetchall()

    close_connect(connection)

    return data

def get_file_path_by_id(id):
    exec = "SELECT file_name FROM TURNIRS AS t WHERE t.id = @0"

    connection, cursor = open_connect()

    cursor.execute(exec, [id])
    r = cursor.fetchone()[0]

    close_connect(connection)

    return r


def get_tur_name_by_id(id):
    exec = "SELECT t.name FROM TURNIRS AS t WHERE t.id = @0"

    connection, cursor = open_connect()

    cursor.execute(exec, [id])
    r = cursor.fetchone()[0]

    close_connect(connection)

    return r