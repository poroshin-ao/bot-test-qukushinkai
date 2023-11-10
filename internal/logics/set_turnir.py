from internal.models.SQLite_db.set_fight import set_new_mf, set_end_fight
from internal.models.SQLite_db.set_member import set_winner_by_id
from internal.models.SQLite_db.set_category import set_cat_newstate_by_id
from internal.drawers.draw_setka import draw_setka, get_mas_setka
from internal.models.SQLite_db.get_category_setka import get_cat_by_m_id, get_members_by_id
from internal.models.SQLite_db.get_turnir import get_tur_name_by_id
from internal.models.SQLite_db.get_category_setka import get_catname_by_id

def set_winner_db(f_id, mw_id, tur_id):
    set_winner_by_id(mw_id)
    c_id = get_cat_by_m_id(mw_id)
    set_cat_newstate_by_id(c_id)
    members = get_members_by_id(c_id)

    set_end_fight(f_id)
    set_new_mf(mw_id, f_id)
    tname = get_tur_name_by_id(tur_id)
    cname = get_catname_by_id(c_id)

    img_path = draw_setka(tur_id,tname,c_id, cname, members)

    return img_path
