#main python file

from flask import Flask, render_template, request, redirect, url_for, session, abort
import sqlite3
from db_init import init_db
import os

app=Flask(__name__)
app.secret_key = 'nicolethebest'

def connect_db():
    db_path = os.path.join(os.path.dirname(__file__), 'bakingContest.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

SECURITY_RULES = {
    'myContestResults': 1,
    'add_entryinfo': 1,
    'list_users': 2,
    'add_user': 3,
    'list_results': 3,
}

@app.before_request
def enforce_security():
    # Skip checks for login page, static files, or undefined endpoints
    if request.endpoint in ['login', 'static', None]:
        return

    # Check if the user is logged in
    username = session.get('username')
    securityLevel = session.get('securityLevel')

    if not username or not securityLevel:
        # If not logged in, redirect to the login page
        return redirect(url_for('login'))

    # Check if the requested route requires a higher SecurityLevel
    required_level = SECURITY_RULES.get(request.endpoint)
    if required_level and securityLevel < required_level:
        # If user lacks permissions, return default "Page Not Found" error
        abort(404)


@app.route('/')
def home():
    username = session.get('username')
    securityLevel = session.get('securityLevel')

    if not username:
        return redirect(url_for('login'))  # Redirect if not logged in
    
    conn = connect_db()
    user = conn.execute('SELECT name FROM new_user WHERE username = ?', (username,)).fetchone()
    conn.close()

    if not user:
        # If the user is not found, clear the session and redirect to login
        session.clear()
        return redirect(url_for('login'))

    name = user['name']

    options = []
    if securityLevel == 1:
        options = [
            ('Show my Contest Entry Results', 'myContestResults'),
            ('Add new Baking Contest Entry', 'add_entryinfo'),
            ('Log out', 'logout')
        ]
    elif securityLevel == 2:
        options = [
            ('Show my Contest Entry Results', 'myContestResults'),
            ('Add new Baking Contest Entry', 'add_entryinfo'),
            ('List Baking Contest Users', 'list_users'),
            ('Log out', 'logout')
        ]
    elif securityLevel == 3:
        options = [
            ('Show my Contest Entry Results', 'myContestResults'),
            ('Add new Baking Contest User', 'add_user'),
            ('Add new Baking Contest Entry', 'add_entryinfo'),
            ('List Baking Contest Users', 'list_users'),
            ('Baking Contest Entry Results', 'list_results'),
            ('Log out', 'logout')
        ]

    return render_template('home.html', name=name, options=options)


@app.route ('/add_user', methods = ['GET', 'POST'])
def add_user():
    msg = ""
    if request.method == 'POST':
        name = request.form.get ('name', '').strip()
        age = request.form.get ('age', '').strip()
        phoneNumber = request.form.get ('phoneNumber', '').strip()
        securityLevel = request.form.get ('securityLevel', '').strip()
        password = request.form.get ('password', '').strip()
        username = request.form.get('username', '').strip()

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
                         INSERT INTO new_user (name, age, phoneNumber, securityLevel, password, username)
                         VALUES (?,?,?,?,?,?)
                         ''', (name, age, phoneNumber, securityLevel, password, username))
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

#project 6 routes

@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        conn = connect_db()
        cursor = conn.execute(
            'SELECT * FROM new_user WHERE username = ? AND password = ?',
            (username, password)
        )
        user = cursor.fetchone()
        conn.close()

        if user:
            session['username'] = user['username']
            session['securityLevel'] = user['securityLevel']
            return redirect(url_for('home'))
        else:
            msg = "invalid username and/or password!"
    
    return render_template('login.html', msg=msg)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/myContestResults')
def myContestResults():
    conn = connect_db()
    results = conn.execute('SELECT nameOfItem, numExcellentVotes, numOkVotes, numBadVotes FROM contest_results LIMIT 4').fetchall()
    conn.close()
    for row in results:
        print(dict(row))   
    return render_template('myContestResults.html', results = results)

@app.route('/add_entryinfo', methods = ['GET','POST'])
def add_entryinfo():
    msg = ""
    if request.method == 'POST':
        nameOfItem = request.form.get('nameOfItem', '').strip()
        numExcellentVotes = request.form.get('numExcellentVotes', '').strip()
        numOkVotes = request.form.get('numOkVotes', '').strip()
        numBadVotes = request.form.get('numBadVotes', '').strip()

        #validate inputs
        error_msg = []

        if not nameOfItem:
            error_msg.append("Query cannot return an empty name.")
        if not numExcellentVotes.isdigit() or not (0 < int(numExcellentVotes)):
            error_msg.append("Query cannot return an integer less than zero.")
        if not numOkVotes.isdigit() or not (0 <int(numOkVotes)):
            error_msg.append("Query cannot return an integer less than zero.")
        if not numBadVotes.isdigit() or not (0 < int(numBadVotes)):
            error_msg.append("Query cannot return an integer less than zero.")
        
        if error_msg:
            error_message = "Query Result: <br>" + "<br>".join(error_msg)
            return render_template('results.html', msg = error_message)
        else:
            conn = connect_db()
            conn.execute('''
                        INSERT INTO contest_results (nameOfItem, numExcellentVotes, numOkVotes, numBadVotes)
                        VALUES (?,?,?,?)
                        ''', (nameOfItem, numExcellentVotes, numOkVotes, numBadVotes))
            conn.commit()
            conn.close()

            msg = "Query Result : Record successfully added"
            return render_template('results.html', msg = msg)

    return render_template('add_entryinfo.html', msg = msg)


if __name__ == '__main__':
    init_db()
    print("Database initialized successfully.")
    app.run(port = 50001, debug = True)


