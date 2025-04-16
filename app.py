import werkzeug
from flask import Flask, render_template, request, url_for, session, redirect, g, abort, send_file, render_template_string
import sqlite3
from random import getrandbits
from func import *
import base64
#Вот сюда тебе и надо, начинающий мастер OSINT'а! Только не смотри другие флаги: кто посмотрит, тот ***** :>


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

@app.route("/osint/found_me", methods=('GET', 'POST'))
def osintfound():
    Y0u_Fin4ly_F0und_7his = 'C4TchFl4g{Pls_supp0rt_my_pr0j3ct}'
    if request.method == 'POST':
        user_flag = request.form['user_flag']
        if user_flag == Y0u_Fin4ly_F0und_7his:
            return render_template('found-me.html', flag=Y0u_Fin4ly_F0und_7his, success_flag='.')
        return render_template('found-me.html', flag=Y0u_Fin4ly_F0und_7his, error='Ошибка: неверный флаг!')
    return render_template('found-me.html')

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

idor_main_users = {}

@app.route("/web/idor", methods=('GET', 'POST'))
def webidor():
    if request.method == 'POST':
        if 'user_flag' in request.form.keys():
            flag = session.get('idor_flag')
            user_flag = request.form['user_flag']
            if user_flag == flag and 'idor_id' in session.keys() and session['idor_id'] in idor_main_users.keys():
                del idor_main_users[session['idor_id']]
                return render_template('idor.html', flag=flag, success_flag='.')
            return render_template('idor.html', flag=flag, error='Ошибка: неверный флаг!')

        login = request.form['login']
        mail =  request.form['mail']
        password = request.form['pass']
        if not login:
            return render_template('idor.html', error='Ошибка: не оставляйте себя без имени!')
        if not password:
            return render_template('idor.html', error='Ошибка: Пароль важен, заполните поле!')

        session['idor_flag'] = f'C4TchFl4g{{{hex(getrandbits(45))[2:]}}}'
        session['idor_id'] = id = getrandbits(8)
        idor_main_users[id] = {'login': login,'mail': mail}
        return redirect(url_for('webidor_user', id=session['idor_id']), code=302)
    return render_template('idor.html')


@app.route("/web/idor/user_id<int:id>", methods=('GET', 'POST'))
def webidor_user(id):
    if 'idor_id' not in session.keys():
        abort(404)
    if id <= 32:
        idor_users = {0: ('admin', 'popa'), 1: ('an', 'fffff'), 2: ('adm', 'qweqewqeqweqwe'), 3: ('admin', session['idor_flag']), 4: ('admin', ''), 5: ('admin', ''), 6: ('admin', ''), 7: ('admin', ''), 8: ('admin', ''), 9: ('admin', ''), 10: ('admin', ''), 11: ('admin', ''), 12: ('admin', ''), 13: ('admin', ''), 14: ('admin', ''), 15: ('admin', '')}
        return render_template('idor_user.html', user=idor_users[id])
    if id not in idor_main_users.keys():
        abort(404)
    return render_template('idor-main-user.html', login=idor_main_users[id]['login'], mail=idor_main_users[id]['mail'])


@app.route("/web/path-traversal", methods=('GET', 'POST'))
def webpt():
    flag_task3 = 'С4Tch_Fl4g{Y0u_Find_4_littl3_kitty}'
    if request.method == 'POST':
        user_flag = request.form['user_flag']
        if user_flag == flag_task3:
            return render_template('path-traversal.html', flag=flag_task3, success_flag='.')
        return render_template('path-traversal.html', flag=flag_task3, error='Ошибка: неверный флаг!')
    filename = request.args.get("file")
    if not filename:
        return render_template('path-traversal.html')
    try:
        return send_file(filename)
    except FileNotFoundError:
        abort(404)

@app.route("/web/ssti", methods=('GET', 'POST'))
def webssti():
    id = session.get('ssti_id')
    flag = session.get('flag_ssti')
    if id not in comments.keys():
        session['ssti_id'] = id = hex(getrandbits(45))[2:]
        comments[id] = []
        session['flag_ssti'] = flag = f'C4TchFl4g{{{hex(getrandbits(45))[2:]}}}'

    if request.method == 'POST':
        if 'user_flag' in  request.form.keys():
            user_flag = request.form['user_flag']
            if user_flag == flag:
                return render_template('ssti.html', flag=flag, success_flag='.')
            return render_template('ssti.html', flag=flag, error='Ошибка: неверный флаг!')

        username = request.form['username']
        comment = request.form['user_comment']
        comments[id].append((username, comment))
    def render(x):
        try:
            return render_template_string(x, flag=flag)
        except:
            return x
    return render_template('ssti.html', render_template_string=render, comments=comments[id], flag=flag)


comments = {}


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



@app.route("/osint/mapmaster", methods=('GET', 'POST'))
def osintgeoguessr():
    flag_task6 = "C4TchFl4g{1905}"
    if request.method == 'POST':
        user_flag = request.form['user_flag']
        if user_flag == flag_task6:
            return render_template('mapmaster.html', flag=flag_task6, success_flag='.')
        return render_template('mapmaster.html', flag=flag_task6, error='Ошибка: неверный флаг!')
    return render_template('mapmaster.html')

@app.route("/osint/really_hard_task", methods=('GET', 'POST'))
def osintrht():
    flag_task7 = "C4TchFl4g{13ts_p14y_min3cr4ft_t0g3th3r}"
    if request.method == 'POST':
        user_flag = request.form['user_flag']
        if user_flag == flag_task7:
            return render_template('osint-hardtask.html', flag=flag_task7, success_flag='.')
        return render_template('osint-hardtask.html', flag=flag_task7, error='Ошибка: неверный флаг!')
    return render_template('osint-hardtask.html')



@app.errorhandler(werkzeug.exceptions.HTTPException)
def error_handler(e):
    return f'<img src="https://http.cat/{e.code}.jpg">', e.code

app.run(host="0.0.0.0", debug=False)
connection.close()
