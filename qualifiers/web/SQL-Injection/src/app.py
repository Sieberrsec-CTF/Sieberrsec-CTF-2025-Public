from flask import Flask, request, render_template, redirect, url_for, g, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = os.urandom(16)  # Necessary for session management

DATABASE = 'users.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    if not os.path.exists(DATABASE):
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute('''CREATE TABLE users (username TEXT, password TEXT)''')
        c.execute("INSERT INTO users VALUES ('admin', 'ALSIFHMOEUGYO#@TY#&RYr3o87ynor87nyo*&NYO*YO*YRO#*&@')")
        conn.commit()
        conn.close()
        print("[+] users.db created with default admin user.")

@app.route('/', methods=['GET', 'POST'])
def login():
    query = ""
    error = ""
    db_error = ""

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # 🚨 Intentionally vulnerable to SQL injection
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        print(f"[DEBUG] Executing query: {query}")

        try:
            cursor = get_db().cursor()
            cursor.execute(query)
            result = cursor.fetchone()

            if result:
                session['authenticated'] = True
                session['username'] = result[0]
                return redirect(url_for('vault'))
            else:
                error = "Access denied."
        except sqlite3.Error as e:
            db_error = str(e)
            error = "SQL error occurred."

    return render_template('login.html', error=error, query=query, db_error=db_error)

@app.route('/vault')
def vault():
    if session.get('authenticated') and session.get('username') == 'admin':
        flag = os.getenv("FLAG")
        return render_template('vault.html', flag=flag)
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
    init_db()
    app.run('0.0.0.0', 12085)
