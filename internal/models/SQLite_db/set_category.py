import sqlite3
from internal.models.SQLite_db.db_connect import *
from internal.models.SQLite_db.set_member import set_member

def set_category(tur_name, tur_date, cat, members):
    connection, cursor = open_connect()

    cat_exec = "INSERT INTO CATEGORIES(t_id, category, state) VALUES ((SELECT id FROM TURNIRS WHERE name = @0 AND date = @1), @2, @3)"
    cursor.execute(cat_exec, [tur_name, tur_date, cat, 0])

    close_connect(connection)

    for m in members:
        set_member(cat, m)


def set_cat_newstate_by_id(c_id):
    exec = "UPDATE CATEGORIES SET state = state + 1 WHERE id = @0"

    connection, cursor = open_connect()

    cursor.execute(exec, [c_id])

    close_connect(connection)


def set_cat_newstate_by_m_id(m_id):
    exec = "UPDATE CATEGORIES SET state = state + 1 WHERE id IN (SELECT m.c_id FROM MEMBERS AS m JOIN CATEGORIES AS c ON m.c_id = c.id WHERE m.id = @0);"

    connection, cursor = open_connect()

    cursor.execute(exec, [m_id])

    close_connect(connection)