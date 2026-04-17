import sqlite3
from model import predict_label
from datetime import datetime

# ===== MODE SELECTION =====
print("Select Mode:")
print("1. Daily")
print("2. Weekly")

choice = input("Enter choice (1 or 2): ")

# connect to database
conn = sqlite3.connect("activity.db")
cursor = conn.cursor()

# ===== APPLY FILTER =====
if choice == "1":
    print("\n--- DAILY REPORT ---")
    cursor.execute("""
        SELECT app_name, timestamp FROM activity_logs
        WHERE DATE(timestamp) = DATE('now')
    """)

elif choice == "2":
    print("\n--- WEEKLY REPORT ---")
    cursor.execute("""
        SELECT app_name, timestamp FROM activity_logs
        WHERE DATE(timestamp) >= DATE('now', '-6 days')
    """)

else:
    print("Invalid choice")
    conn.close()
    exit()

rows = cursor.fetchall()

# ===== EXISTING LOGIC (UNCHANGED) =====

focus_count = 0
distraction_count = 0

hour_data = {}

current_streak = 0
max_streak = 0

for row in rows:
    app_name = row[0]
    timestamp = row[1]

    hour = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S").hour

    if hour not in hour_data:
        hour_data[hour] = {"focus": 0, "distraction": 0}

    label = predict_label(app_name)

    if label == "focus":
        focus_count += 1
        hour_data[hour]["focus"] += 1

        current_streak += 1
        if current_streak > max_streak:
            max_streak = current_streak

    else:
        distraction_count += 1
        hour_data[hour]["distraction"] += 1
        current_streak = 0

# ===== TIME CALCULATION =====

focus_time = focus_count * 5
distraction_time = distraction_count * 5
total_time = focus_time + distraction_time

productivity_score = (focus_time / total_time) * 100 if total_time > 0 else 0

# ===== OUTPUT =====

print("\nOverall Analysis")
print("Focus time (sec):", focus_time)
print("Distraction time (sec):", distraction_time)
print("Productivity score:", round(productivity_score, 2), "%")

print("\nHour-wise Analysis:")
for hour in sorted(hour_data.keys()):
    print(f"{hour}:00 → Focus: {hour_data[hour]['focus']} | Distraction: {hour_data[hour]['distraction']}")

print("\nFocus Streak:")
print("Max Focus Streak:", max_streak)

# ===== SMART INSIGHTS =====

print("\nSmart Insights:")

if productivity_score < 50:
    print("Your productivity is low. Try reducing distractions.")
else:
    print("Good productivity! Keep it up.")

if distraction_count > focus_count:
    print("You are spending more time on distracting activities.")
else:
    print("You are mostly focused.")

if max_streak < 3:
    print("Your focus streak is low. Try to stay consistent.")
else:
    print("Good focus streak! Maintain it.")

for hour in hour_data:
    if hour_data[hour]["distraction"] > hour_data[hour]["focus"]:
        print(f"You are more distracted around {hour}:00.")

conn.close()