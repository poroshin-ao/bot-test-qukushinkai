from internal.models.SQLite_db.db_connect import *


def delete_members_tur_id(id):
    exec = "DELETE FROM MEMBERS AS m WHERE m.id in (SELECT m.id FROM MEMBERS AS m JOIN CATEGORIES AS c ON c.id = m.c_id JOIN TURNIRS AS t ON c.t_id = t.id WHERE t.id = @0)"

    connection, cursor = open_connect()

    cursor.execute(exec, [id])

    close_connect(connection)


def delete_teleg_id_by_m_id(m_id, tel_id):
    exec = "DELETE FROM MEMB_TEL AS mt WHERE mt.m_id = @0 AND mt.tel_id = @1"

    connection, cursor = open_connect()

    cursor.execute(exec, [m_id, tel_id])

    close_connect(connection)