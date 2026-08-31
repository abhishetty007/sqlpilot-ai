import sqlite3
from pathlib import Path

UPLOAD_FOLDER = Path(__file__).resolve().parent.parent / "uploaded_databases"


def get_schema(database_name):

    # Frontend may send "shakila" or "shakila.db"
    database_name = Path(database_name).name

    if not database_name.lower().endswith(".db"):
        database_name += ".db"

    db_path = UPLOAD_FOLDER / database_name

    print("SCHEMA DATABASE PATH:", db_path)
    print("DATABASE EXISTS:", db_path.exists())

    if not db_path.exists():
        raise Exception(f"Database not found: {db_path}")

    conn = sqlite3.connect(str(db_path))

    try:
        cur = conn.cursor()

        cur.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
            AND name NOT LIKE 'sqlite_%'
            ORDER BY name
        """)

        tables = cur.fetchall()

        print("TABLES FOUND:", tables)

        if not tables:
            raise Exception(
                f"No tables found in database '{database_name}'"
            )

        schema = []

        for (table,) in tables:

            safe_table = table.replace('"', '""')

            cur.execute(
                f'PRAGMA table_info("{safe_table}")'
            )

            columns = [
                row[1]
                for row in cur.fetchall()
            ]

            schema.append(
                f"{table}({', '.join(columns)})"
            )

        return "\n".join(schema)

    finally:
        conn.close()