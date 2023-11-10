from internal.logics.delete_fight import delete_fights_by_tur_id
from internal.models.SQLite_db.delete_member import delete_members_tur_id, delete_teleg_id_by_m_id


def delete_members_by_tur_id(id):
    delete_fights_by_tur_id(id)
    delete_members_tur_id(id)

def delete_tel_id_by_m_id(m_id, tel_id):
    delete_teleg_id_by_m_id(m_id, tel_id)