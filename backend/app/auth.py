import sqlite3
import bcrypt
from pathlib import Path

# ============================================================
# DATABASE
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
DB_FILE = BASE_DIR / "main_app.db"


def get_conn():
    return sqlite3.connect(str(DB_FILE))


# ============================================================
# INITIALIZE USERS TABLE
# ============================================================

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


# ============================================================
# CREATE ACCOUNT
# ============================================================

def signup(username: str, password: str):

    username = username.strip()

    if not username:
        return False, "Username is required."

    if not password:
        return False, "Password is required."

    if len(username) < 3:
        return False, "Username must be at least 3 characters."

    if len(password) < 6:
        return False, "Password must be at least 6 characters."

    conn = get_conn()

    try:

        # Check whether username already exists
        existing = conn.execute(
            "SELECT id FROM users WHERE username = ?",
            (username,)
        ).fetchone()

        if existing:
            return False, "Username already exists."

        # Hash password
        hashed = bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt()
        )

        conn.execute(
            """
            INSERT INTO users (username, password)
            VALUES (?, ?)
            """,
            (username, hashed)
        )

        conn.commit()

        return True, "Account created successfully!"

    except sqlite3.IntegrityError:

        return False, "Username already exists."

    except Exception as e:

        return False, str(e)

    finally:

        conn.close()


# ============================================================
# LOGIN
# ============================================================

def login(username: str, password: str):

    username = username.strip()

    conn = get_conn()

    try:

        cur = conn.cursor()

        cur.execute(
            """
            SELECT id, password
            FROM users
            WHERE username = ?
            """,
            (username,)
        )

        row = cur.fetchone()

    finally:

        conn.close()

    if row is None:
        return False, None

    user_id = row[0]
    stored_password = row[1]

    try:

        if bcrypt.checkpw(
            password.encode("utf-8"),
            stored_password
        ):
            return True, user_id

    except (ValueError, TypeError):

        pass

    return False, None