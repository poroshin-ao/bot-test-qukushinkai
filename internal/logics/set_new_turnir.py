from internal.models.data_files.data_files import download_file, parse_from_file
from internal.models.SQLite_db.set_turnir import set_turnir
from internal.models.SQLite_db.get_turnir import get_fullturnir_by_name_date
from internal.drawers.draw_setka import get_mas_setka, draw_setka
from internal.models.SQLite_db.set_fight import set_new_fight
from internal.models.SQLite_db.get_fight import get_fight_num_by_m
from datetime import datetime


async def set_new_tur(data):
    now = datetime.now()
    strdate = "data_" + now.strftime("%Y_%m_%d_%H_%M_%S") +".xlsx"
    strdate = ".\\storage\\data_turnir\\"+strdate

    await download_file(data['tur_data_path'], strdate)
    data_file = parse_from_file(strdate)
    set_turnir(data,data_file,strdate)

    tur_data = get_fullturnir_by_name_date(data["tur_name"], data["tur_date"])
    
    d_setkas = dict()
    for tur, c in tur_data.items():
        d_setkas[tur] = dict()
        for cat, m in c.items():
            pust_mas = []
            d_setkas[tur][cat] = get_mas_setka(m,pust_mas)
    
    r_max = get_max_rounds(d_setkas) - 1
    num = 1
    while r_max > 0:
        for tur, c in d_setkas.items():
            for cat, m in c.items():
                l = len(m)
                if l > r_max-1:
                    for i in range(len(m[l-r_max])):
                        if not m[l-r_max][i] is None:
                            if m[l-r_max][i]["id"] < 0:
                                m[l-r_max][i]["fio"] = "№"+str(num)
                                set_new_fight(num,m[l-r_max-1][i*2]["id"],m[l-r_max-1][i*2+1]["id"])
                                f_id = get_fight_num_by_m(m[l-r_max-1][i*2]["id"],m[l-r_max-1][i*2+1]["id"])["id"]
                                m[l-r_max][i]["id"] = -f_id
                                num = num+1 
        r_max = r_max-1
    
    img_paths = []

    for tur, c in tur_data.items():
        for cat, m in c.items():    
            img_paths.append(draw_setka(tur[0], tur[1], cat[0], cat[1], m))
    
    return img_paths

def get_max_rounds(d_setkas):
    r_max = 0
    for tur, c in d_setkas.items():
        for cat, m in c.items():
            if len(m)>r_max:
                r_max = len(m)
    return r_max
