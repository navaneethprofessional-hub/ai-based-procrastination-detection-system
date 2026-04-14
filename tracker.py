import pygetwindow as gw
import sqlite3
import time
from datetime import datetime

# connect to database
conn = sqlite3.connect("activity.db")
cursor = conn.cursor()

# create table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS activity_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    app_name TEXT,
    timestamp TEXT
)
""")
conn.commit()

# function to clean window title
def clean_name(title):
    name = title.lower()

    # detect coding tools
    if "visual studio code" in name:
        return "VS Code"

    # detect notepad
    if "notepad" in name:
        return "Notepad"

    # detect pdf files
    if ".pdf" in name:
        return "PDF"

    # detect youtube categories
    if "youtube" in name:
        if "python" in name:
            return "YT Python"
        elif "sql" in name:
            return "YT SQL"
        elif "recipe" in name or "food" in name or "fried rice" in name:
            return "YT Food"
        elif "trailer" in name or "movie" in name:
            return "YT Movie"
        elif "song" in name or "music" in name:
            return "YT Music"
        elif "ipl" in name or "cricket" in name:
            return "YT IPL"
        elif "game" in name or "gaming" in name:
            return "YT Gaming"
        else:
            return "YouTube"

    # detect games
    if "hill climb" in name:
        return "Hill Climb Racing"

    # fallback: take first meaningful part
    return title.split("-")[0].strip()


# continuously track active window
while True:
    try:
        window = gw.getActiveWindow()

        # get active window title and clean it
        if window and window.title:
            raw_title = window.title.strip()
            app_name = clean_name(raw_title)
        else:
            app_name = "Unknown"

        # ignore unknown entries
        if app_name.lower() == "unknown":
            time.sleep(5)
            continue

        # get current timestamp
        time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # insert into database
        cursor.execute(
            "INSERT INTO activity_logs (app_name, timestamp) VALUES (?, ?)",
            (app_name, time_now)
        )

        conn.commit()

        print("Tracked:", app_name, time_now)

    except Exception as e:
        print("Error:", e)

    # wait 5 seconds before next tracking
    time.sleep(5)