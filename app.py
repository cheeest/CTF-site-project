import werkzeug
from flask import Flask, render_template, request, url_for, session, redirect, g, abort, send_file
import sqlite3
from random import getrandbits
from func import *
import base64

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

@app.route("/web")
def web():
    return render_template('web-main.html')

@app.route("/forensic")
def forensic():
    return render_template('forensic-main.html')

@app.route("/osint")
def osint():
    return render_template('osint-main.html')

@app.route("/web/sql-injection", methods=('GET', 'POST'))
def websql():
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

@app.route("/web/idor")
def webidor():
    return render_template('idor.html')

@app.route("/web/path-traversal")
def webpt():
    return render_template('path-traversal.html')

@app.route("/web/ssti")
def webssti():
    return render_template('ssti.html')

@app.route("/web/portswigger-guide")
def webpsguide():
    return render_template('portswigger-guide.html')

@app.route("/forensic/metadata", methods=('GET', 'POST'))
def fmetadata():
    flag_task1 = session.get('flag_task1')
    if request.method == 'POST':
        user_flag = request.form['user_flag']
        if user_flag == flag_task1:
            return render_template('task1-metadata.html', flag=flag_task1, success_flag='.')
        return render_template('task1-metadata.html', flag=flag_task1, error='Ошибка: неверный флаг!')

    if not flag_task1:
        session['task1_id'] = id = hex(getrandbits(45))[2:]
        session['flag_task1'] = flag_task1 = f'C4TchFl4g{{{hex(getrandbits(45))[2:]}}}'
        task1_flag(flag_task1, id)
    return render_template('task1-metadata.html', flag=flag_task1)

@app.route("/forensic/getimg")
def forensic_task1():
    if 'task1_id' not in session.keys():
        abort(404)
    return send_file(f'/tmp/task1/{session['task1_id']}.jpg')

@app.route("/forensic/base-guide", methods=('GET', 'POST'))
def fbase():
    flag_task4 = session.get('flag_task4')
    if request.method == 'POST':
        user_flag = request.form['user_flag']
        if user_flag == flag_task4:
            return render_template('base.html', flag=flag_task4, success_flag='.')
        return render_template('base.html', flag=flag_task4, error='Ошибка: неверный флаг!')
    if not flag_task4:
        session['flag_task4'] = flag_task4 = f'C4TchFl4g{{{hex(getrandbits(45))[2:]}}}'
    base32str = str(base64.b32encode(flag_task4.encode()))[2:-1]
    base64str = str(base64.b64encode(f"Ой-ой, похоже, что самое главное всё ещё зашифровано.. Сможешь расшифровать, ОП?  {base32str}".encode()))[2:-1]
    return render_template('base.html', base_task=base64str)


@app.route("/forensic/.docx_files", methods=('GET', 'POST'))
def fbinwalk():
    flag_task3 = 'C4TchFl4g{GT4_6_1eaks}'
    if request.method == 'POST':
        user_flag = request.form['user_flag']
        if user_flag == flag_task3:
            return render_template('binwalk.html', flag=flag_task3, success_flag='.')
        return render_template('binwalk.html', flag=flag_task3, error='Ошибка: неверный флаг!')
    return render_template('binwalk.html')

@app.route("/forensic/hex", methods=('GET', 'POST'))
def fhex():
    flag_task2 = "C4TchFl4g{I_hir3d_7his_c4r_t0_st4r3_4t_Y0u}"
    if request.method == 'POST':
        user_flag = request.form['user_flag']
        if user_flag == flag_task2:
            return render_template('hex.html', flag=flag_task2, success_flag='.')
        return render_template('hex.html', flag=flag_task2, error='Ошибка: неверный флаг!')
    return render_template('hex.html')

@app.route("/forensic/hash", methods=('GET', 'POST'))
def fhash():
    flag_task5 = "C4TchFl4g{superadmin}"
    if request.method == 'POST':
        user_flag = request.form['user_flag']
        if user_flag == flag_task5:
            return render_template('hash.html', flag=flag_task5, success_flag='.')
        return render_template('hash.html', flag=flag_task5, error='Ошибка: неверный флаг!')
    return render_template('hash.html')

@app.route("/osint/questions")
def osintquestions():
    return render_template('osint-questions.html')

@app.route("/osint/geoguessr")
def osintgeoguessr():
    return render_template('osint-geoguessr.html')

@app.route("/osint/really_hard_task")
def osintrht():
    return render_template('osint-hardtask.html')

@app.route("/web/success_login-sqltask", methods=('GET', 'POST'))
def success_login():
    flag = session.get('sql_flag')
    if request.method == 'POST':
        user_flag = request.form['user_flag']
        if user_flag == flag:
            return render_template('success-sql.html', flag=flag, success_flag='.')
        return render_template('success-sql.html', flag=flag, error='Ошибка: неверный флаг!')
    if flag:
        return render_template('success-sql.html', flag=flag)
    abort(404)

@app.errorhandler(werkzeug.exceptions.NotFound)
def handle_bad_request(e):
    return '<img src="https://http.cat/404.jpg">', 404

app.run(host="0.0.0.0", debug=False)
connection.close()
