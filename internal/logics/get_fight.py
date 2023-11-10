from internal.models.SQLite_db.get_fight import get_notendedfight_with_members_by_id,  get_notendedfight_member_by_id_pnum_f

def get_spisok_to_win(id, f_num):
    l = len(get_notendedfight_with_members_by_id(id))
    if l > f_num*2:
        return get_notendedfight_with_members_by_id(id)[f_num*2]
    return None

def get_last_2_and_5_fight(id):
    m2 = get_notendedfight_member_by_id_pnum_f(id, 3)
    m5 = get_notendedfight_member_by_id_pnum_f(id, 6)
    m = []
    if len(m2) != 0:
        m.append(m2)
    else:
        m.append(None)
    if len(m5) != 0:
        m.append(m5)
    else:
        m.append(None)
    if len(m) == 0:
        return None
    return m