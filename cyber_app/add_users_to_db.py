import sqlite3
import hashlib
import json

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def add_user_to_db(login, password, email):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    hashed_password = hash_password(password)
    try:
        cursor.execute(
            '''INSERT INTO users (login, password, email) VALUES (?, ?, ?)''',
            (login, hashed_password, email)
        )
    except sqlite3.IntegrityError:
        print(f"User {login} already exists or email {email} is duplicate.")
    conn.commit()
    conn.close()

def import_users_from_json(json_file):
    with open(json_file, "r") as file:
        users = json.load(file)
    for user in users:
        add_user_to_db(user['login'], user['password'], user['email'])

if __name__ == "__main__":
    import_users_from_json("users.json")
    print("Users successfully imported into the database.")
