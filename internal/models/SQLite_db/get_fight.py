from internal.models.SQLite_db.db_connect import *

def get_fight_num_by_m(m1_id, m2_id):
    connection, cursor = open_connect()

    exec_m_m= "SELECT f.id, f.num_f FROM FIGHTS AS f INNER JOIN MEMB_FIGH AS mf1 ON mf1.f_id=f.id INNER JOIN MEMB_FIGH as mf2 ON f.id = mf2.f_id WHERE mf1.m_id = @0 AND mf2.m_id = @1"
    exec_m_f= "SELECT f.id, f.num_f FROM FIGHTS AS f INNER JOIN MEMB_FIGH AS mf1 ON mf1.f_id=f.id INNER JOIN FIGH_FIGH as ff2 ON f.id = ff2.f_id WHERE mf1.m_id = @0 AND ff2.f = @1"
    exec_f_m= "SELECT f.id, f.num_f FROM FIGHTS AS f INNER JOIN FIGH_FIGH AS ff1 ON ff1.f_id=f.id INNER JOIN MEMB_FIGH as mf2 ON f.id = mf2.f_id WHERE ff1.f = @0 AND mf2.m_id = @1"
    exec_f_f= "SELECT f.id, f.num_f FROM FIGHTS AS f INNER JOIN FIGH_FIGH AS ff1 ON ff1.f_id=f.id INNER JOIN FIGH_FIGH as ff2 ON f.id = ff2.f_id WHERE ff1.f = @0 AND ff2.f = @1"
    
    if m1_id > 0:
        if m2_id > 0:
            cursor.execute(exec_m_m, [m1_id, m2_id])
        else:
            cursor.execute(exec_m_f, [m1_id, -m2_id])            
    else:
        if m2_id > 0:
            cursor.execute(exec_f_m, [-m1_id, m2_id])
        else:
            cursor.execute(exec_f_f, [-m1_id, -m2_id])

    num_f = cursor.fetchone()

    if num_f is None:
        return None

    close_connect(connection)

    return {"id":num_f[0], "fio": num_f[1]}

def get_fight_by_tur_id(id):
    exec = "SELECT f.id FROM FIGHTS AS f \
        JOIN MEMB_FIGH AS mf ON f.id=mf.f_id \
        JOIN MEMBERS AS m ON m.id = mf.m_id \
        JOIN CATEGORIES AS c ON c.id = m.c_id \
        JOIN TURNIRS AS t ON t.id = c.t_id \
        WHERE t.id = @0"
    
    connection, cursor = open_connect()

    cursor.execute(exec, [id])
    d = cursor.fetchall()

    close_connect(connection)
    return d

def get_notendedfight_with_members_by_id(id):
    exec = "SELECT f.id, f.num_f, m1.id, m1.fio, m2.id, m2.fio \
        FROM FIGHTS AS f \
        JOIN MEMB_FIGH AS mf1 ON mf1.f_id = f.id \
        JOIN MEMB_FIGH AS mf2 ON mf2.f_id = f.id \
        JOIN MEMBERS AS m1 ON m1.id = mf1.m_id \
        JOIN MEMBERS AS m2 ON m2.id = mf2.m_id \
        JOIN CATEGORIES AS c ON m1.c_id = c.id \
        JOIN TURNIRS AS t ON t.id = c.t_id \
        WHERE t.id = @0 AND mf1.f_id = mf2.f_id AND NOT mf1.m_id = mf2.m_id AND f.is_end = 0 \
        ORDER BY f.num_f"
    
    connection, cursor = open_connect()

    cursor.execute(exec, [id])
    data = cursor.fetchall()

    close_connect(connection)

    return data


def get_notendedfight_member_by_id_pnum_f(id, pnum_f):
    exec2 = "SELECT COUNT(*) FROM FIGHTS AS f \
        JOIN MEMB_FIGH AS mf ON mf.f_id = f.id \
        JOIN MEMBERS AS m ON m.id = mf.m_id \
        JOIN CATEGORIES AS c ON m.c_id = c.id \
        JOIN TURNIRS AS t ON t.id = c.t_id \
        WHERE t.id = @0 AND f.is_end = 1"
    
    exec = "SELECT m.id\
        FROM FIGHTS AS f \
        JOIN MEMB_FIGH AS mf ON mf.f_id = f.id \
        JOIN MEMBERS AS m ON m.id = mf.m_id \
        JOIN CATEGORIES AS c ON m.c_id = c.id \
        JOIN TURNIRS AS t ON t.id = c.t_id \
        WHERE t.id = @0 AND \
        f.num_f = @1 + @2 \
        ORDER BY f.num_f"
    
    connection, cursor = open_connect()

    cursor.execute(exec2, [id])
    count = cursor.fetchone()[0]
    if count is None:
        count = 0
    cursor.execute(exec, [id, pnum_f, int(count/2)])
    data = cursor.fetchall()

    close_connect(connection)

    return data