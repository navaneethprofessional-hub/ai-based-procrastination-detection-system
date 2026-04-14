import sqlite3

# connect to database
conn = sqlite3.connect("activity.db")
cursor = conn.cursor()

# fetch all records
cursor.execute("SELECT * FROM activity_logs")
rows = cursor.fetchall()

# display data in readable format
for row in rows:
    print(f"ID: {row[0]} | App: {row[1]} | Time: {row[2]}")

# close connection
conn.close()