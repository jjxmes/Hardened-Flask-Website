#main python file

from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from db_init import init_db
import os

app=Flask(__name__)

def connect_db():
    db_path = os.path.join(os.path.dirname(__file__), 'bakingContest.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def home():
    return render_template('home.html')


@app.route ('/add_user', methods = ['GET', 'POST'])
def add_user():
    msg = ""
    if request.method == 'POST':
        name = request.form.get ('name', '').strip()
        age = request.form.get ('age', '').strip()
        phoneNumber = request.form.get ('phoneNumber', '').strip()
        securityLevel = request.form.get ('securityLevel', '').strip()
        password = request.form.get ('password', '').strip()

        #validate inputs:
        error_msg = []

        if not name:
            error_msg.append("You can not enter in an empty name")
        if not age.isdigit() or not (0 < int(age) < 121):
            error_msg.append("The Age must be a whole number greater than 0 and less than 121.")
        if not phoneNumber:
            error_msg.append("You can not enter in a empty phone number")
        if not securityLevel.isdigit() or not (1 <= int(securityLevel) <= 3):
            error_msg.append("The SecurityLevel must be a numeric between 1 and 3.")
        if not password:
            error_msg.append("You can not enter in an empty pwd")

        if error_msg:
            error_message = "Query Result: <br>" + "<br>".join(error_msg)
            return render_template('results.html', msg = error_message)
        else:
            #Insert the new user into the database
            conn = connect_db()
            conn.execute('''
                         INSERT INTO new_user (name, age, phoneNumber, securityLevel, password)
                         VALUES (?,?,?,?,?)
                         ''', (name, age, phoneNumber, securityLevel, password))
            conn.commit()
            conn.close()

            msg = "Query Result : Record successfully added"

            return render_template('results.html', msg = msg)
           

    return render_template('add_user.html', msg = msg)

@app.route ('/list_users')
def list_users():
    conn = connect_db()
    users = conn.execute('SELECT * FROM new_user').fetchall()
    conn.close()
    return render_template('list_users.html', users = users)

@app.route ('/list_results')
def list_results():
    conn = connect_db()
    results = conn.execute('SELECT * FROM contest_results LIMIT 4').fetchall()
    conn.close()
    for row in results:
        print (dict(row))
    return render_template('list_results.html', results = results)


@app.route ('/results')
def results():
    msg = request.args.get('msg', '')
    return render_template('results.html', msg = msg)

if __name__ == '__main__':
    init_db()
    print("Database initialized successfully.")
    app.run(port = 50003, debug = True)

