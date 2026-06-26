"""
db.py - Dynamic Multi-Database Manager
All tables stored in one SQLite file. Supports built-in + user-created tables.
"""

import sqlite3
import json
import shutil
import os

MAIN_DB = "main_app.db"

BUILTIN_DATABASES = {
    "🎓 Students": {
        "table": "students",
        "description": "Student marks and records",
        "schema_text": "  id     INTEGER PRIMARY KEY\n  name   TEXT\n  marks  INTEGER",
        "columns": ["id", "name", "marks"],
        "init_sql": """CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL, marks INTEGER NOT NULL);""",
        "sample": ("INSERT INTO students (name, marks) VALUES (?, ?)", [
            ("Abhinandan",92),("Abhishek",85),("Riya",78),("Kiran",55),
            ("Priya",67),("Rahul",90),("Sneha",45),("Arjun",73),
            ("Divya",88),("Rohit",61),
        ]),
    },
    "📚 Library": {
        "table": "books",
        "description": "Books, authors, and availability",
        "schema_text": "  id        INTEGER PRIMARY KEY\n  title     TEXT\n  author    TEXT\n  genre     TEXT\n  available INTEGER",
        "columns": ["id", "title", "author", "genre", "available"],
        "init_sql": """CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL, author TEXT NOT NULL,
            genre TEXT NOT NULL, available INTEGER NOT NULL DEFAULT 1);""",
        "sample": ("INSERT INTO books (title, author, genre, available) VALUES (?, ?, ?, ?)", [
            ("The Alchemist","Paulo Coelho","Fiction",1),
            ("A Brief History of Time","Stephen Hawking","Science",0),
            ("Sapiens","Yuval Noah Harari","History",1),
            ("Clean Code","Robert C. Martin","Tech",1),
            ("Atomic Habits","James Clear","Self-Help",0),
            ("1984","George Orwell","Fiction",0),
            ("Thinking Fast and Slow","Daniel Kahneman","Psychology",1),
            ("Deep Work","Cal Newport","Self-Help",1),
        ]),
    },
    "🏥 Hospital": {
        "table": "patients",
        "description": "Patients and doctor records",
        "schema_text": "  id      INTEGER PRIMARY KEY\n  name    TEXT\n  age     INTEGER\n  disease TEXT\n  doctor  TEXT",
        "columns": ["id", "name", "age", "disease", "doctor"],
        "init_sql": """CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL, age INTEGER NOT NULL,
            disease TEXT NOT NULL, doctor TEXT NOT NULL);""",
        "sample": ("INSERT INTO patients (name, age, disease, doctor) VALUES (?, ?, ?, ?)", [
            ("Ramesh",45,"Diabetes","Dr. Sharma"),("Sita",32,"Hypertension","Dr. Mehta"),
            ("Arun",60,"Arthritis","Dr. Sharma"),("Pooja",28,"Migraine","Dr. Rao"),
            ("Vikram",52,"Diabetes","Dr. Mehta"),("Lakshmi",41,"Asthma","Dr. Rao"),
            ("Gopal",35,"Fever","Dr. Sharma"),("Anita",55,"Diabetes","Dr. Mehta"),
        ]),
    },
}


def get_connection():
    return sqlite3.connect(MAIN_DB)


def init_meta_table():

    conn = get_connection()

    conn.execute("""
    CREATE TABLE IF NOT EXISTS _custom_tables (
        name TEXT,
        user_id INTEGER,

        source_name TEXT,
        source_type TEXT,

        label TEXT NOT NULL,
        description TEXT,
        columns_json TEXT NOT NULL,

        PRIMARY KEY(name, user_id)
    )
    """)

    conn.commit()

    conn.close()


def init_all_dbs():

    init_meta_table()

    conn = get_connection()
    cur = conn.cursor()

    # ============================================
    # Initialize built-in databases
    # ============================================

    for cfg in BUILTIN_DATABASES.values():

        cur.executescript(cfg["init_sql"])

        cur.execute(f"SELECT COUNT(*) FROM {cfg['table']}")

        if cur.fetchone()[0] == 0:

            sql, rows = cfg["sample"]

            cur.executemany(sql, rows)

    # ============================================
    # Query History Table
    # ============================================

    cur.execute("""
CREATE TABLE IF NOT EXISTS query_history (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    user_id INTEGER,

    user_query TEXT,

    generated_sql TEXT,

    source TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
    """)

    conn.commit()
    conn.close()


def create_custom_table(
    table_name: str,
    label: str,
    columns: list,
    description: str = "",
    user_id=None
):

    conn = get_connection()

    try:

        col_defs = ["id INTEGER PRIMARY KEY AUTOINCREMENT"]

        col_names = ["id"]

        for col in columns:

            col_defs.append(
                f"{col['name']} {col['type']}"
            )

            col_names.append(
                col["name"]
            )


        conn.execute(
            f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(col_defs)})"
        )


        conn.execute(
            """
            INSERT OR REPLACE INTO _custom_tables
            (
                name,
                user_id,
                source_name,
                source_type,
                label,
                description,
                columns_json
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                table_name,
                user_id,
                "Manual Tables",
                "manual",
                label,
                description,
                json.dumps(col_names)
            )
        )


        conn.commit()

        return True, f"Table '{table_name}' created successfully!"


    except Exception as e:

        return False, str(e)


    finally:

        conn.close()

def import_csv_table(
    df,
    table_name: str,
    label: str,
    description: str = "",
    user_id=None,
    source_name=None,
    source_type="file"
):

    conn = get_connection()

    try:

        table_name = (
            table_name
            .strip()
            .lower()
            .replace(" ", "_")
            .replace("-", "_")
            .replace("(", "_")
            .replace(")", "_")
        )

        # Clean column names
        df.columns = [
            str(c).strip().lower().replace(" ", "_")
            for c in df.columns
        ]
        table_name = (
            table_name
            .strip()
            .lower()
            .replace(" ", "_")
            .replace("-", "_")
        )
        # Store dataframe into SQLite
        df.to_sql(
            table_name,
            conn,
            if_exists="replace",
            index=False
        )

        # Build metadata
        columns = list(df.columns)

        schema_lines = "\n".join(
            [f"  {c}  TEXT" for c in columns]
        )

        # Register table
        conn.execute(
            """
INSERT OR REPLACE INTO _custom_tables
(name, user_id, source_name, source_type, label, description, columns_json)
VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
(
    table_name,
    user_id,
    source_name,
    source_type,
    label,
    description,
    json.dumps(columns)
)
        )

        conn.commit()

        return True, f"Imported '{table_name}' successfully!"

    except Exception as e:

        return False, str(e)

    finally:

        conn.close()


def delete_custom_table(
    table_name: str,
    user_id
):
    conn = get_connection()
    try:
        conn.execute(f"DROP TABLE IF EXISTS {table_name}")
        conn.execute(
    """
    DELETE FROM _custom_tables
    WHERE name = ?
    AND user_id = ?
    """,
    (
        table_name,
        user_id
    )
)
        conn.commit()
        return True, "Table deleted."
    except Exception as e:
        return False, str(e)
    finally:
        conn.close()


def get_custom_tables(user_id=None) -> dict:

    conn = get_connection()

    cur = conn.cursor()

    cur.execute(
        """
        SELECT 
            name,
            label,
            description,
            columns_json,
            source_name,
            source_type
        FROM _custom_tables
        WHERE user_id=?
        """,
        (user_id,)
    )

    rows = cur.fetchall()


    conn.close()

    result = {}

    for name, label, desc, cols_json, source_name, source_type in rows:

        columns = json.loads(cols_json)

        result[label] = {
            "table": name,
            "description": desc,
            "columns": columns,
            "custom": True,
            "source_name": source_name,
            "source_type": source_type
        }

    return result


def get_all_databases(user_id=None) -> dict:

    d = dict(BUILTIN_DATABASES)

    d.update(
        get_custom_tables(user_id)
    )

    return d


def get_schema(db_label: str, user_id=None) -> str:
    cfg = get_all_databases(user_id).get(db_label, {})
    return (f"Table: {cfg.get('table','?')}\n"
            f"Description: {cfg.get('description','')}\n"
            f"Columns:\n{cfg.get('schema_text','')}\n")


def run_query(db_label: str, sql: str, query_type: str = "SELECT"):
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(sql)
        if query_type.upper() == "SELECT":
            rows = cur.fetchall()
            cols = [d[0] for d in cur.description]
            return rows, cols, 0
        elif query_type.upper() == "CREATE":
            conn.commit()
            return [], [], 0
        else:
            conn.commit()
            return [], [], cur.rowcount
    finally:
        conn.close()


def get_table_data(db_label: str, user_id=None):
    cfg = get_all_databases(user_id).get(db_label, {})
    table = cfg.get("table", "")
    if not table:
        return [], []
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {table}")
    rows = cur.fetchall()
    cols = [d[0] for d in cur.description]
    conn.close()
    return rows, cols
# existing code above
def save_query_history(
    user_id,
    user_query,
    generated_sql,
    source
):

    conn = get_connection()

    conn.execute(
        """
        INSERT INTO query_history (
    user_id,
    user_query,
    generated_sql,
    source
)
VALUES (?, ?, ?, ?)
        """,
        (
            user_id,
            user_query,
            generated_sql,
            source
        )
    )

    conn.commit()

    conn.close()


def get_query_history(user_id):

    conn = get_connection()

    rows = conn.execute(
        """
        SELECT user_query, generated_sql, source
        FROM query_history
        WHERE user_id=?
        ORDER BY id DESC
        """,
        (user_id,)
    ).fetchall()

    conn.close()

    return rows


def import_sqlite_database(
    uploaded_db_path,
    user_id
):

    source = sqlite3.connect(uploaded_db_path)

    target = get_connection()

    try:

        tables = source.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type='table'
            """
        ).fetchall()

        imported = []

        for (table,) in tables:

            df = __import__("pandas").read_sql_query(
                f"SELECT * FROM {table}",
                source
            )

            new_name = f"user_{user_id}_{table}"

            df.to_sql(
                new_name,
                target,
                if_exists="replace",
                index=False
            )

            columns = list(df.columns)

            target.execute(
                """
                INSERT OR REPLACE INTO _custom_tables
                (
                    name,
                    user_id,
                    source_name,
                    source_type,
                    label,
                    description,
                    columns_json
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    new_name,
                    user_id,
                    uploaded_db_path.split("\\")[-1],
                    "sqlite",
                    f"📋 {table}",
                    "Imported SQLite table",
                    json.dumps(columns)
                )
            )

            imported.append(table)

        target.commit()

        return True, imported


    except Exception as e:

        return False, str(e)


    finally:

        source.close()

        target.close()