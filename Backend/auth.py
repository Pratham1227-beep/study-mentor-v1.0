import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE,
        password TEXT
    )
    """)
    conn.commit()
    conn.close()

def register_user(email, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    hashed = generate_password_hash(password)
    try:
        c.execute("INSERT INTO users (email, password) VALUES (?,?)",
                  (email, hashed))
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()

def login_user(email, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT password FROM users WHERE email=?", (email,))
    user = c.fetchone()
    conn.close()
    return user and check_password_hash(user[0], password)
