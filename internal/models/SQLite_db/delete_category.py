from internal.models.SQLite_db.db_connect import *


def delete_categories_tur_id(id):
    exec = "DELETE FROM CATEGORIES AS c WHERE c.id in (SELECT c.id FROM CATEGORIES AS c JOIN TURNIRS AS t ON t.id = c.t_id WHERE t.id = @0)"

    connection, cursor = open_connect()

    cursor.execute(exec, [id])

    close_connect(connection)