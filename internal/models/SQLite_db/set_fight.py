from internal.models.SQLite_db.db_connect import *


def set_new_fight(num_f,id_m1, id_m2):
    connect, cursor = open_connect()

    exec_f = "INSERT INTO FIGHTS(num_f) VALUES(@0)"
    exec_s = "SELECT last_insert_rowid();"
    exec_m_f = "INSERT INTO MEMB_FIGH(m_id, f_id) VALUES(@0, @1)"
    exec_f_f = "INSERT INTO FIGH_FIGH(f, f_id) VALUES(@0, @1)"

    cursor.execute(exec_f, [num_f])
    cursor.execute(exec_s)
    id_f = cursor.fetchone()[0]

    connect.commit()

    if id_m1 < 0:
        cursor.execute(exec_f_f, [-id_m1, id_f])
    else:
        cursor.execute(exec_m_f, [id_m1, id_f])
    if id_m2 < 0:
        cursor.execute(exec_f_f,[-id_m2, id_f])
    else:
        cursor.execute(exec_m_f,[id_m2, id_f])

    cursor.execute(exec_s)
    r = cursor.fetchone()[0]
    close_connect(connect)
    return r

def set_end_fight(f_id):
    exec = "UPDATE FIGHTS AS f SET is_end = 1 WHERE f.id = @0"

    connection, cursor = open_connect()

    cursor.execute(exec, [f_id])

    close_connect(connection)

def set_new_mf(m_id, f_id):
    exec_s = "SELECT ff.f_id FROM FIGH_FIGH AS ff WHERE ff.f = @0"
    exec_d = "DELETE FROM FIGH_FIGH AS ff WHERE ff.f_id = @0 AND ff.f = @1"
    exec_a = "INSERT INTO MEMB_FIGH(m_id, f_id) VALUES(@0, @1)"

    connection, cursor = open_connect()

    cursor.execute(exec_s, [f_id])
    ff_id = cursor.fetchone()
    if not ff_id is None:

        cursor.execute(exec_d, [ff_id[0], f_id])
        cursor.execute(exec_a, [m_id, ff_id[0]])

    close_connect(connection)