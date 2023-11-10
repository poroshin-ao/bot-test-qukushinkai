from internal.models.SQLite_db.get_turnir import get_turnir_name_place_date
from internal.models.SQLite_db.get_turnir import get_turid_catid_stage
from internal.models.SQLite_db.get_turnir import get_tur_data_by_id


def get_turnir_name_date():
    return get_turnir_name_place_date()

def get_id_tur_by_num(num):
    data = get_turnir_name_place_date()
    try:
        return data[num-1][3]
    except Exception:
        return -1

def get_path_setki(id):
    data = get_turid_catid_stage(id)
    paths = [] 
    for p in data:
        paths.append(str(p[0])+"_"+str(p[1])+"_"+str(p[2]))
    
    return paths

def get_turnir_data_by_id(id):
    return get_tur_data_by_id(id)