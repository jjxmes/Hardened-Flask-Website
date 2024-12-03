#database initialization file

import sqlite3

def init_db():
    conn = sqlite3.connect ('bakingContest.db')
    cursor = conn.cursor()

    with open('baking.sql', 'r') as f:
        sql_script = f.read()

    cursor.executescript(sql_script)

    cursor.execute('DELETE FROM new_user')

    cursor.execute('''
        INSERT INTO new_user (name, age, phoneNumber, securityLevel, password, username)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', ('Test User', 30, '1234567890', 3, 'password', 'test'))

    conn.commit()
    conn.close()


