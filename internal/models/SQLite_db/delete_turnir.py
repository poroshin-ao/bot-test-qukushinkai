from internal.models.SQLite_db.db_connect import *


def delete_turnir_id(id):
    exec = "DELETE FROM TURNIRS WHERE id = @0"

    connection, cursor = open_connect()

    cursor.execute(exec, [id])

    close_connect(connection)