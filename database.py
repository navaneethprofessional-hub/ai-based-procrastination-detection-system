import sqlite3

# connect to database (creates file if not exists)
conn = sqlite3.connect("activity.db")

cursor = conn.cursor()

# create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS activity_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    app_name TEXT,
    timestamp TEXT
)
""")

conn.commit()
conn.close()

print("Database and table created successfully")