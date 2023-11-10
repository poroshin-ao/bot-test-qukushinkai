from internal.models.SQLite_db.db_connect import *

def member_is_exist(fio):
    exec = "SELECT id FROM MEMBERS WHERE fio = @0"

    connection, cursor = open_connect()

    cursor.execute(exec, [fio])
    id = cursor.fetchone()

    close_connect(connection)
    if id is None:
        return None
    return id[0]

def get_turid_catid_state_by_id(id):
    exec = "SELECT c.t_id, c.id, c.state FROM MEMBERS AS m JOIN CATEGORIES AS c ON c.id = m.c_id WHERE m.id = @0"

    connection ,cursor = open_connect()

    cursor.execute(exec, [id])
    data = cursor.fetchone()

    close_connect(connection)
    return data

def get_notendedfight_with_members_by_id_m_id(tur_id, m_id):
    exec = "SELECT f.id, f.num_f, m1.id, m1.fio, m2.id, m2.fio \
        FROM FIGHTS AS f \
        JOIN MEMB_FIGH AS mf1 ON mf1.f_id = f.id \
        JOIN MEMB_FIGH AS mf2 ON mf2.f_id = f.id \
        JOIN MEMBERS AS m1 ON m1.id = mf1.m_id \
        JOIN MEMBERS AS m2 ON m2.id = mf2.m_id \
        JOIN CATEGORIES AS c ON m1.c_id = c.id \
        JOIN TURNIRS AS t ON t.id = c.t_id \
        WHERE t.id = @0 AND mf1.f_id = mf2.f_id AND NOT mf1.m_id = mf2.m_id AND f.is_end = 0 AND m1.id = @1 \
        ORDER BY f.num_f"
    
    connection, cursor = open_connect()

    cursor.execute(exec, [tur_id, m_id])
    data = cursor.fetchone()

    close_connect(connection)

    return data

def get_memb_id_by_tel_id(id):
    exec = "SELECT m.id FROM MEMB_TEL AS mt JOIN MEMBERS AS m ON m.id = mt.m_id WHERE mt.tel_id = @0"

    connection, cursor = open_connect()

    cursor.execute(exec, [id])
    data = cursor.fetchone()

    close_connect(connection)
    if data is None:
        return None
    return data[0]

def get_teleg_id_by_m_id(m_id):
    exec = "SELECT tel_id FROM MEMB_TEL WHERE m_id = @0"

    connection, cursor = open_connect()

    cursor.execute(exec, [m_id])
    data = cursor.fetchall()

    close_connect(connection)

    return data

