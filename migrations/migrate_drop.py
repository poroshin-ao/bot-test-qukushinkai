import sqlite3

def go_migrate():
    with open('.\migrations\migrate_drop.sql', 'r') as sql_file:
        sql_script = sql_file.read()

    connection = sqlite3.connect(".\storage\data_base\database.db")
    cursor = connection.cursor()

    cursor.executescript(sql_script)

    connection.commit()
    connection.close()

if __name__ == '__main__':
    go_migrate()