import sqlite3

# connect to database
conn = sqlite3.connect("activity.db")
cursor = conn.cursor()

# fetch all records
cursor.execute("SELECT * FROM activity_logs")
rows = cursor.fetchall()

# display data
for row in rows:
    print(row)

# close connection
conn.close()