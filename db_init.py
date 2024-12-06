#database initialization file

import sqlite3
import  string, base64
import Encryption

def init_db():
    conn = sqlite3.connect ('bakingContest.db')
    cursor = conn.cursor()

    with open('baking.sql', 'r') as f:
        sql_script = f.read()

    cursor.executescript(sql_script) 
    conn.commit()

    cursor.execute('DELETE FROM new_user')

    username = str(Encryption.cipher.encrypt(b'user3').decode("utf-8"))
    password = str(Encryption.cipher.encrypt(b'password3').decode("utf-8"))
    phoneNumber = str(Encryption.cipher.encrypt(b'3333333333').decode("utf-8"))
    cursor.execute('''
        INSERT INTO new_user (name, age, phoneNumber, securityLevel, password, username)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', ('User3', 30, phoneNumber, 3, password, username))
    conn.commit()

    username = str(Encryption.cipher.encrypt(b'user2').decode("utf-8"))
    password = str(Encryption.cipher.encrypt(b'password2').decode("utf-8"))
    phoneNumber = str(Encryption.cipher.encrypt(b'2222222222').decode("utf-8"))
    cursor.execute('''
        INSERT INTO new_user (name, age, phoneNumber, securityLevel, password, username)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', ('User2', 30, phoneNumber, 2, password, username))
    conn.commit()

    username = str(Encryption.cipher.encrypt(b'user1').decode("utf-8"))
    password = str(Encryption.cipher.encrypt(b'password1').decode("utf-8"))
    phoneNumber = str(Encryption.cipher.encrypt(b'1111111111').decode("utf-8"))
    cursor.execute('''
        INSERT INTO new_user (name, age, phoneNumber, securityLevel, password, username)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', ('User1', 30, phoneNumber, 1, password, username))
    conn.commit()

    conn.close()


