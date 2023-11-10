from internal.models.SQLite_db.get_member import member_is_exist, get_turid_catid_state_by_id, get_notendedfight_with_members_by_id_m_id
from internal.models.SQLite_db.get_member import get_memb_id_by_tel_id
from internal.models.SQLite_db.get_member import get_teleg_id_by_m_id


def memb_is_exist(fio):
    return member_is_exist(fio)

def get_path_img_by_id(id):
    data = get_turid_catid_state_by_id(id)
    return str(data[0]) + "_" + str(data[1]) + "_" +str(data[2]) +".jpg"

def get_spisok_to_win(tur_id, m_id):
    return get_notendedfight_with_members_by_id_m_id(tur_id, m_id)

def get_m_id_by_tel_id(tel_id):
    return get_memb_id_by_tel_id(tel_id)

def get_tel_id_by_m_id(m_id):
    return get_teleg_id_by_m_id(m_id)