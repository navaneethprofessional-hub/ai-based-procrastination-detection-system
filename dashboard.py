import streamlit as st
import sqlite3
from model import predict_label
import pandas as pd
from datetime import datetime
import plotly.express as px

st.title("AI Productivity Dashboard")

# ---------------- MODE ----------------
mode = st.selectbox("Select View", ["Daily", "Weekly"])

# ---------------- DATABASE ----------------
conn = sqlite3.connect("activity.db")
cursor = conn.cursor()

if mode == "Daily":
    cursor.execute("""
        SELECT app_name, timestamp FROM activity_logs
        WHERE DATE(timestamp) = DATE('now')
    """)
else:
    cursor.execute("""
        SELECT app_name, timestamp FROM activity_logs
        WHERE DATE(timestamp) >= DATE('now', '-6 days')
    """)

rows = cursor.fetchall()

if not rows:
    st.warning("No data available")
    st.stop()

# ---------------- CLEAN ----------------
def clean_name(name):
    name = name.lower()
    if "visual studio" in name:
        return "VS Code"
    if "youtube" in name:
        if "movie" in name:
            return "YT Movie"
        return "YouTube"
    return name.split("-")[0].strip()

# ---------------- PROCESS ----------------
focus_count = 0
distraction_count = 0

app_focus = {}
app_distraction = {}

hour_data = {}
day_data = {}

current_streak = 0
max_streak = 0
streak_day = ""

for row in rows:
    raw = row[0]
    ts = row[1]

    app = clean_name(raw)
    label = predict_label(raw)

    dt = datetime.strptime(ts, "%Y-%m-%d %H:%M:%S")
    hour = dt.hour
    day = dt.strftime("%A")

    if hour not in hour_data:
        hour_data[hour] = {"focus": 0, "distraction": 0}

    if day not in day_data:
        day_data[day] = {"focus": 0, "distraction": 0}

    if label == "focus":
        focus_count += 1
        app_focus[app] = app_focus.get(app, 0) + 1

        hour_data[hour]["focus"] += 1
        day_data[day]["focus"] += 1

        current_streak += 1
        if current_streak > max_streak:
            max_streak = current_streak
            streak_day = day

    else:
        distraction_count += 1
        app_distraction[app] = app_distraction.get(app, 0) + 1

        hour_data[hour]["distraction"] += 1
        day_data[day]["distraction"] += 1

        current_streak = 0

# ---------------- CALCULATIONS ----------------
focus_time = focus_count * 5
distraction_time = distraction_count * 5
total_time = focus_time + distraction_time

score = (focus_time / total_time) * 100 if total_time else 0

# ---------------- OVERALL ----------------
st.subheader("Overall Statistics")
st.write(f"Focus Time: {focus_time}")
st.write(f"Distraction Time: {distraction_time}")
st.write(f"Total Time: {total_time}")
st.write(f"Productivity Score: {round(score,2)}%")

# ---------------- PIE ----------------
st.subheader("Focus vs Distraction")

pie = px.pie(
    names=["Focus", "Distraction"],
    values=[focus_time, distraction_time],
    color=["Focus", "Distraction"],
    color_discrete_map={
        "Focus": "#90EE90",
        "Distraction": "#FF9999"
    }
)
st.plotly_chart(pie, use_container_width=True)

# ---------------- LINE ----------------
st.subheader("Trend Analysis")

if mode == "Daily":
    df = pd.DataFrame(hour_data).T.reset_index()
    df.columns = ["Hour", "Focus", "Distraction"]

    fig = px.line(
        df, x="Hour", y=["Focus", "Distraction"],
        color_discrete_map={"Focus": "#90EE90", "Distraction": "#FF9999"}
    )

else:
    df = pd.DataFrame(day_data).T.reset_index()
    df.columns = ["Day", "Focus", "Distraction"]

    fig = px.line(
        df, x="Day", y=["Focus", "Distraction"],
        color_discrete_map={"Focus": "#90EE90", "Distraction": "#FF9999"}
    )

st.plotly_chart(fig, use_container_width=True)

# ---------------- BAR ----------------
st.subheader("Bar Analysis")

if mode == "Daily":
    data = []
    for app in set(app_focus) | set(app_distraction):
        data.append({
            "App": app,
            "Focus": app_focus.get(app, 0),
            "Distraction": app_distraction.get(app, 0)
        })

    df = pd.DataFrame(data)

    fig = px.bar(
        df, x="App", y=["Focus", "Distraction"],
        color_discrete_map={"Focus": "#90EE90", "Distraction": "#FF9999"}
    )

else:
    df = pd.DataFrame(day_data).T.reset_index()
    df.columns = ["Day", "Focus", "Distraction"]

    fig = px.bar(
        df, x="Day", y=["Focus", "Distraction"],
        color_discrete_map={"Focus": "#90EE90", "Distraction": "#FF9999"}
    )

st.plotly_chart(fig, use_container_width=True)

# ---------------- INSIGHTS ----------------
st.subheader("Personal Insights")

focus_pct = (focus_time/total_time)*100 if total_time else 0
dis_pct = (distraction_time/total_time)*100 if total_time else 0

most_used = max(app_focus, key=app_focus.get) if app_focus else "N/A"
most_dis = max(app_distraction, key=app_distraction.get) if app_distraction else "N/A"

behavior = "Focused" if focus_count > distraction_count else "Distracted"
productivity = "Good" if score > 50 else "Low"

# ---------------- DAILY INSIGHTS ----------------
if mode == "Daily":

    peak_hour = max(hour_data, key=lambda x: hour_data[x]["distraction"])

    st.write(f"Most Used App: {most_used}")
    st.write(f"Most Distracting App: {most_dis}")
    st.write(f"Focus Percentage: {round(focus_pct,2)}%")
    st.write(f"Distraction Percentage: {round(dis_pct,2)}%")
    st.write(f"Behavior: {behavior}")
    st.write(f"Productivity: {productivity}")
    st.write(f"Peak Distraction Time: {peak_hour}:00")
    st.write(f"Max Focus Streak: {max_streak}")
    st.write(f"Total Sessions: {len(rows)}")
    st.write(f"Recommendation: Reduce usage of {most_dis}")

# ---------------- WEEKLY INSIGHTS ----------------
else:

    peak_day = max(day_data, key=lambda x: day_data[x]["distraction"])

    st.write(f"Most Used App: {most_used}")
    st.write(f"Most Distracting App: {most_dis}")
    st.write(f"Focus Percentage: {round(focus_pct,2)}%")
    st.write(f"Distraction Percentage: {round(dis_pct,2)}%")
    st.write(f"Behavior: {behavior}")
    st.write(f"Productivity: {productivity}")
    st.write(f"Peak Distraction Day: {peak_day}")
    st.write(f"Max Focus Streak: {max_streak} ({peak_day})")
    st.write(f"Total Sessions: {len(rows)}")
    st.write(f"Recommendation: Reduce usage of {most_dis}")

conn.close()