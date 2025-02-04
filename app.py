import werkzeug
from flask import Flask, render_template, request, url_for, session, redirect, g, abort
import sqlite3
from random import getrandbits

connection = sqlite3.connect('database.db')
cursor = connection.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
    id INTEGER PRIMARY KEY,
    login TEXT NOT NULL,
    password TEXT NOT NULL
    )
''')
cursor.execute('SELECT * FROM Users where login = "admin"')
if not cursor.fetchone():
    cursor.execute('INSERT INTO Users (login, password) VALUES (?, ?)', ('admin', '12345678'))
connection.commit()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ca4ac4ada05f91a5790d2132992bfaed86df15c4d08f2dfe'
DATABASE = 'database.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db:
        db.close()

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/sql-injection", methods=('GET', 'POST'))
def sql():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['pass']
        cursor = get_db().cursor()
        cursor.execute(f'SELECT * FROM Users WHERE login == "{login}" AND password == "{password}"')
        user = cursor.fetchone()
        if not user:
            return render_template('sql-injection.html', error='Ошибка: неверный логин или пароль')
        session['sql_flag'] = f'C4TchFl4g{{{hex(getrandbits(45))[2:]}}}'
        return redirect(url_for('success_login'), code=302)
    return render_template('sql-injection.html')

@app.route("/found-me")
def found():
    return render_template('found.html')

@app.route("/decode-me")
def decode():
    return render_template('decode.html')

@app.route("/success_login", methods=('GET', 'POST'))
def success_login():
    flag = session.get('sql_flag')
    if request.method == 'POST':
        user_flag = request.form['user_flag']
        if user_flag == flag:
            return render_template('success.html', flag=flag, success_flag='.')
        return render_template('success.html', flag=flag, error='Ошибка: неверный флаг!')
    if flag:
        return render_template('success.html', flag=flag)
    abort(404)

@app.errorhandler(werkzeug.exceptions.NotFound)
def handle_bad_request(e):
    return '<img src="https://http.cat/404.jpg">', 404

app.run(host="0.0.0.0", debug=False)
connection.close()
