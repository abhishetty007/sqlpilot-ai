import sqlite3
import bcrypt
from pathlib import Path

# Absolute path to backend/main_app.db
BASE_DIR = Path(__file__).resolve().parent.parent
DB_FILE = BASE_DIR / "main_app.db"


def get_conn():
    return sqlite3.connect(str(DB_FILE))


def init_users_table():
    conn = get_conn()

    conn.execute("""
    CREATE TABLE IF NOT EXISTS users (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        username TEXT UNIQUE NOT NULL,

        password BLOB NOT NULL

    )
    """)

    conn.commit()
    conn.close()


def signup(username, password):
    conn = get_conn()

    try:
        hashed = bcrypt.hashpw(
            password.encode(),
            bcrypt.gensalt()
        )

        conn.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, hashed)
        )

        conn.commit()

        return True, "Account created successfully!"

    except Exception as e:
        return False, str(e)

    finally:
        conn.close()


def login(username, password):
    conn = get_conn()

    cur = conn.cursor()

    cur.execute(
        "SELECT id, password FROM users WHERE username=?",
        (username,)
    )

    row = cur.fetchone()

    conn.close()

    if row is None:
        return False, None

    user_id = row[0]
    stored_password = row[1]

    if bcrypt.checkpw(password.encode(), stored_password):
        return True, user_id

    return False, None