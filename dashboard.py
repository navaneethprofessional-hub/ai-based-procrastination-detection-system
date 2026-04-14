import streamlit as st
import sqlite3
from model import predict_label
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

st.title("AI Productivity Dashboard")

# connect to database
conn = sqlite3.connect("activity.db")
cursor = conn.cursor()

cursor.execute("SELECT app_name, timestamp FROM activity_logs")
rows = cursor.fetchall()

focus_count = 0
distraction_count = 0

app_focus = {}
app_distraction = {}

time_data = {}

# ---------------- PROCESS DATA ----------------
for row in rows:
    app_name = row[0]
    timestamp = row[1]

    label = predict_label(app_name)

    # count totals
    if label == "focus":
        focus_count += 1
        app_focus[app_name] = app_focus.get(app_name, 0) + 1
    else:
        distraction_count += 1
        app_distraction[app_name] = app_distraction.get(app_name, 0) + 1

    # time grouping (5 min interval)
    time_obj = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
    minute_bucket = (time_obj.minute // 5) * 5
    time_key = f"{time_obj.hour:02d}:{minute_bucket:02d}"

    if time_key not in time_data:
        time_data[time_key] = {"focus": 0, "distraction": 0}

    time_data[time_key][label] += 1

# ---------------- CALCULATIONS ----------------
focus_time = focus_count * 5
distraction_time = distraction_count * 5
total_time = focus_time + distraction_time

productivity_score = (focus_time / total_time) * 100 if total_time > 0 else 0

# ---------------- STATS ----------------
st.subheader("Overall Statistics")
st.write(f"Focus Time: {focus_time} sec")
st.write(f"Distraction Time: {distraction_time} sec")
st.write(f"Productivity Score: {round(productivity_score, 2)} %")

# ---------------- PIE CHART ----------------
st.subheader("Focus vs Distraction")

labels = ["Focus", "Distraction"]
sizes = [focus_time, distraction_time]

fig, ax = plt.subplots()
ax.pie(sizes, labels=labels, autopct="%1.1f%%")
ax.axis("equal")

st.pyplot(fig)

# ---------------- LINE CHART ----------------
st.subheader("Focus vs Distraction Trend (5-min intervals)")

time_list = []
for t in sorted(time_data.keys()):
    time_list.append({
        "Time": t,
        "Focus": time_data[t]["focus"],
        "Distraction": time_data[t]["distraction"]
    })

time_df = pd.DataFrame(time_list).set_index("Time")
st.line_chart(time_df)

# ---------------- BAR CHART ----------------
st.subheader("Focus vs Distraction by Application")

all_apps = set(list(app_focus.keys()) + list(app_distraction.keys()))

app_data = []
for app in all_apps:
    app_data.append({
        "App": app,
        "Focus": app_focus.get(app, 0),
        "Distraction": app_distraction.get(app, 0)
    })

app_df = pd.DataFrame(app_data)
st.bar_chart(app_df.set_index("App"))

# ---------------- CLEAN DISPLAY FUNCTION ----------------
def clean_display_name(app_name):
    name = app_name.lower()

    name = name.replace("- google chrome", "")
    name = name.replace("- chrome", "")

    if "youtube" in name:
        if "sql" in name:
            return "YouTube (SQL)"
        elif "python" in name:
            return "YouTube (Python)"
        elif "game" in name or "free fire" in name:
            return "YouTube (Gaming)"
        else:
            return "YouTube"

    if "visual studio" in name or "code" in name:
        return "VS Code"

    if "github" in name:
        return "GitHub"

    return name.split()[0].capitalize()

# ---------------- PERSONAL INSIGHTS ----------------
st.subheader("Personal Insights")

# most used app
app_counts = {}
for row in rows:
    app = row[0]
    app_counts[app] = app_counts.get(app, 0) + 1

most_used_app = max(app_counts, key=app_counts.get)
most_used_app_clean = clean_display_name(most_used_app)

# most distracting app
most_distracting_app = max(app_distraction, key=app_distraction.get) if app_distraction else "None"
most_distracting_app_clean = clean_display_name(most_distracting_app)

# percentages
focus_percentage = (focus_time / total_time) * 100 if total_time > 0 else 0
distraction_percentage = 100 - focus_percentage

# peak distraction time
peak_distraction_time = max(time_data, key=lambda x: time_data[x]["distraction"]) if time_data else "N/A"

# focus streak
current_streak = 0
max_streak = 0

for row in rows:
    label = predict_label(row[0])
    if label == "focus":
        current_streak += 1
        max_streak = max(max_streak, current_streak)
    else:
        current_streak = 0

# behavior insight
behavior = "More Focused" if focus_count > distraction_count else "More Distracted"

# productivity insight
productivity_status = "Good" if productivity_score >= 50 else "Low"

# recommendation
recommendation = f"Reduce usage of {most_distracting_app_clean}" if most_distracting_app != "None" else "No major distractions detected"

# display
st.write(f"Most Used App: {most_used_app_clean}")
st.write(f"Most Distracting App: {most_distracting_app_clean}")
st.write(f"Focus Percentage: {round(focus_percentage, 2)}%")
st.write(f"Distraction Percentage: {round(distraction_percentage, 2)}%")
st.write(f"Peak Distraction Time: {peak_distraction_time}")
st.write(f"Max Focus Streak: {max_streak}")
st.write(f"Behavior: {behavior}")
st.write(f"Productivity: {productivity_status}")
st.write(f"Recommendation: {recommendation}")

conn.close()