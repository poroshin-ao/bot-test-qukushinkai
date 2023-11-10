import sqlite3
from internal.models.SQLite_db.db_connect import *

def set_member(cat, member):
    connection, cursor = open_connect()

    mem_exec = "INSERT INTO MEMBERS(c_id, fio, n_fights, n_wons) VALUES ((SELECT id FROM CATEGORIES WHERE category = @0), @1, @2, @3)"
    cursor.execute(mem_exec, [cat, member["FIO"], member["num_fight"] , 0])

    close_connect(connection)

def set_winner_by_id(id):
    exec = "UPDATE MEMBERS SET n_wons = n_wons +1 WHERE id = @0"

    connection, cursor = open_connect()

    cursor.execute(exec, [id])

    close_connect(connection)

def set_member_tel(m_id, tel_id):
    exec = "INSERT INTO MEMB_TEL(m_id, tel_id) VALUES(@0, @1)"

    connection, cursor = open_connect()

    cursor.execute(exec, [m_id, tel_id])

    close_connect(connection)