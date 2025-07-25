from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

with open('flag.txt','r') as f:
    flag = f.read()

def login(username,password):
    # query the database
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        query = f"SELECT username FROM users WHERE username='{username}' AND password='{password}'"
        
        try:
            cur.execute(query)
            found = cur.fetchone()
        except (sqlite3.Error,sqlite3.Warning) as e:
            return f'Login unsuccessful. Error attained: {e}', query
        except:
            return f'Login unsuccessful. Error attained.', query

    # if the username and password checks out, login successful
    # give flag to admin
    if found:
        if found[0] == 'admin':
            return f'Welcome back {found[0]}, here is the flag: {flag}', query
        return f'Login sucessful, welcome back {found}!', query

    # if login unsuccessful
    return 'Login unsuccessful', query

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        result, query = login(username, password)
        return render_template("index.html", result=result, query=query,username=username,password=password)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=False,host='0.0.0.0')
