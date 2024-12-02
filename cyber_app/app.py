from flask import Flask, request, render_template, redirect, url_for, flash, session
import sqlite3
import hashlib

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def validate_user(login, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    hashed_password = hash_password(password)
    try:
        query = f"SELECT * FROM users WHERE login = '{login}' AND password = '{hashed_password}'"
        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()
        return rows
    except Exception as e:
        conn.close()
        return {"error": str(e)}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/user')
def user():
    username = session.get('username', 'User')
    return render_template('user.html', username=username)

@app.route('/hacker')
def hacker():
    return render_template('hacker.html')

@app.route('/login', methods=['POST'])
def login():
    login = request.form['login']
    password = request.form['password']
    user = validate_user(login, password)
    if user:
        session['username'] = user[1]  
        flash(f"Welcome, {user[1]}!", "success")
        return redirect(url_for('user'))
    else:
        flash("Invalid login or password", "danger")
        return redirect(url_for('hacker'))

if __name__ == '__main__':
    app.run(debug=True)
