#  python tracker.py

import pygetwindow as gw
import sqlite3
import time
from datetime import datetime

conn = sqlite3.connect("activity.db")
cursor = conn.cursor()

while True:
    try:
        window = gw.getActiveWindow()

        if window and window.title:
            app_name = window.title
        else:
            app_name = "Unknown"

        time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute(
            "INSERT INTO activity_logs (app_name, timestamp) VALUES (?, ?)",
            (app_name, time_now)
        )

        conn.commit()

        print("Tracked:", app_name, time_now)

    except Exception as e:
        print("Error:", e)

    time.sleep(5)