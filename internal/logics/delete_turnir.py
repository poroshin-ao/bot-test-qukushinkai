from internal.logics.delete_category import delete_categories_by_tur_id
from internal.models.SQLite_db.delete_turnir import delete_turnir_id
from internal.models.SQLite_db.get_turnir import get_file_path_by_id
from internal.models.SQLite_db.get_turnir import get_turid_catid_stage
import os


def delete_tur_by_id(id):
    img_paths = get_turid_catid_stage(id)
    for img in img_paths:
        for s in range(0,img[2]+1):
            os.remove(".\storage\img_setka\setka_"+str(img[0])+"_"+str(img[1])+"_"+str(s)+".jpg")
    delete_categories_by_tur_id(id)
    file_path = get_file_path_by_id(id)
    os.remove(file_path)
    delete_turnir_id(id)
