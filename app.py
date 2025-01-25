from flask import Flask, render_template, request, url_for, flash, redirect
import sqlite3

connection = sqlite3.connect('my_database.db')
cursor = connection.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
    id INTEGER PRIMARY KEY,
    login TEXT NOT NULL,
    password TEXT NOT NULL
    )
''')
cursor.execute('SELECT * FROM Users where login = "admin"')
user = cursor.fetchone()
if not user:
    cursor.execute('INSERT INTO Users (login, password) VALUES (?, ?)', ('admin', '12345678'))
connection.commit()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ca4ac4ada05f91a5790d2132992bfaed86df15c4d08f2dfe'

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/sql-injection", methods=('GET', 'POST'))
def sql():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['pass']
    return render_template('sql-injection.html')

@app.route("/found-me")
def found():
    return render_template('found.html')

@app.route("/decode-me")
def decode():
    return render_template('decode.html')

@app.route("/auth-data")
def authdata():
    pass


app.run()
connection.close()