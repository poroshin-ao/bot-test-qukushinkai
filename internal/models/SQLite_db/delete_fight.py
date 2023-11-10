from internal.models.SQLite_db.db_connect import *
from internal.models.SQLite_db.get_fight import get_fight_by_tur_id

def delete_fights_id(id):
    exec_d_ff = "DELETE FROM FIGH_FIGH AS ff \
        WHERE ff.id IN ( \
        SELECT ff.id FROM FIGH_FIGH AS ff \
        JOIN FIGHTS AS f ON ff.f = f.id \
        JOIN MEMB_FIGH AS mf ON mf.f_id = f.id\
        JOIN MEMBERS AS m ON m.id = mf.m_id \
        JOIN CATEGORIES AS c ON c.id = m.c_id \
        JOIN TURNIRS AS t ON t.id = c.t_id \
        WHERE t.id = @0)"
    
    exec_d_mf = "DELETE FROM MEMB_FIGH AS mf\
        WHERE mf.id IN (\
        SELECT mf.id FROM MEMB_FIGH AS mf \
        JOIN MEMBERS AS m ON mf.m_id = m.id \
        JOIN CATEGORIES AS c ON m.c_id = c.id \
        JOIN TURNIRS AS t ON t.id = c.t_id \
        WHERE t.id = @0)"
    
    exec_d_f = "DELETE FROM FIGHTS AS f \
        WHERE f.id = @0"

    f_ids = get_fight_by_tur_id(id)
    connection, cursor = open_connect()

    cursor.execute(exec_d_ff, [id])
    cursor.execute(exec_d_mf, [id])

    for i in f_ids:
        cursor.execute(exec_d_f, i)

    close_connect(connection) 