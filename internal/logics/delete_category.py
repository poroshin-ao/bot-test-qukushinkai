from internal.logics.delete_member import delete_members_by_tur_id
from internal.models.SQLite_db.delete_category import delete_categories_tur_id


def delete_categories_by_tur_id(id):
    delete_members_by_tur_id(id)
    delete_categories_tur_id(id)