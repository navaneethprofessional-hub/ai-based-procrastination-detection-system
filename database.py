# python database.py

import sqlite3

conn = sqlite3.connect("activity.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM activity_logs")

rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()