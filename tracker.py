import pygetwindow as gw
import sqlite3
import time
from datetime import datetime

# connect to database
conn = sqlite3.connect("activity.db")
cursor = conn.cursor()

# continuously track active window
while True:
    try:
        window = gw.getActiveWindow()

        # get current active window title
        if window and window.title:
            app_name = window.title
        else:
            app_name = "Unknown"

        # get current timestamp
        time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # insert data into database
        cursor.execute(
            "INSERT INTO activity_logs (app_name, timestamp) VALUES (?, ?)",
            (app_name, time_now)
        )

        conn.commit()

        print("Tracked:", app_name, time_now)

    except Exception as e:
        print("Error:", e)

    # track every 5 seconds
    time.sleep(5)