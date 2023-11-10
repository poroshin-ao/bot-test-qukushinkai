from internal.models.SQLite_db.db_connect import *

def get_cat_by_m_id(m_id):
    exec = "SELECT m.c_id FROM MEMBERS AS m WHERE m.id = @0"

    connection, cursor = open_connect()

    cursor.execute(exec, [m_id])
    c_id = cursor.fetchone()

    close_connect(connection)

    return c_id[0]

def get_members_by_id(c_id):
    exec = "SELECT m.id, m.fio, m.n_fights, m.n_wons FROM MEMBERS AS m WHERE m.c_id = @0"

    connection, cursor = open_connect()

    cursor.execute(exec, [c_id])
    members = cursor.fetchall()

    close_connect(connection)

    m = []
    for i in members:
        d = dict()
        d["id"] = i[0]
        d["fio"] = i[1]
        d["n_fights"]=i[2]
        d["n_wons"] = i[3]
        m.append(d)

    return m

def get_state_by_id(id):
    exec = "SELECT state FROM CATEGORIES WHERE id = @0"

    connection, cursor = open_connect()

    cursor.execute(exec, [id])
    state = cursor.fetchone()

    close_connect(connection)

    return state[0]

def get_catname_by_id(id):
    exec = "SELECT category FROM CATEGORIES WHERE id = @0"

    connection, cursor = open_connect()

    cursor.execute(exec, [id])
    state = cursor.fetchone()

    close_connect(connection)

    return state[0]