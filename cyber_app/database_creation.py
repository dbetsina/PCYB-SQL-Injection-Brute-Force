import sqlite3
import hashlib

conn = sqlite3.connect('users.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    login TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE
)
''')

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def add_user(login, password, email):
    hashed_password = hash_password(password)
    try:
        cursor.execute('''INSERT INTO users (login, password, email) VALUES (?, ?, ?)''', (login, hashed_password, email))
        conn.commit()
        print(f"User {login} has been added.")
    except sqlite3.IntegrityError:
        print(f"A user with login {login} or email {email} already exists.")


add_user("user1", "password123", "lol1@example.com")
add_user("user2", "password456", "lol2@example.com")

conn.close()