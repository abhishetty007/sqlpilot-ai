import sqlite3
from pathlib import Path

UPLOAD_FOLDER = Path("uploaded_databases")


def execute_query(database_name, sql):

    db_path = UPLOAD_FOLDER / database_name

    print("EXECUTION DATABASE PATH:", db_path)
    print("DATABASE EXISTS:", db_path.exists())

    if not db_path.exists():
        raise Exception(f"Database not found: {database_name}")

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    try:
        cur = conn.cursor()

        cur.execute(sql)

        rows = [dict(row) for row in cur.fetchall()]

        return rows

    finally:
        conn.close()