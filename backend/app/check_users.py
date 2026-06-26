import sqlite3

conn = sqlite3.connect("main_app.db")

cur = conn.cursor()

cur.execute("SELECT id, username FROM users")

rows = cur.fetchall()

print(rows)

conn.close()