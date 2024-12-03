#database initialization file

import sqlite3

def init_db():
    conn = sqlite3.connect ('bakingContest.db')
    cursor = conn.cursor()

    with open('baking.sql', 'r') as f:
        sql_script = f.read()

    cursor.executescript(sql_script)

    conn.commit()
    conn.close()


