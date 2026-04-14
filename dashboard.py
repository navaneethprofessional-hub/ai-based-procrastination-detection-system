import streamlit as st
import sqlite3
from model import predict_label
import pandas as pd
import matplotlib.pyplot as plt

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

# AI-based classification only
def classify(app_name):
    return predict_label(app_name)

# Main processing
for row in rows:
    app_name = row[0]

    label = classify(app_name)

    if label == "focus":
        focus_count += 1
        app_focus[app_name] = app_focus.get(app_name, 0) + 1
    else:
        distraction_count += 1
        app_distraction[app_name] = app_distraction.get(app_name, 0) + 1

# Calculations
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

# ---------------- APP-WISE BAR CHART ----------------
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

# ---------------- PERSONAL INSIGHTS ----------------
st.subheader("Personal Insights")

# Most used app
app_counts = {}
for row in rows:
    app = row[0]
    app_counts[app] = app_counts.get(app, 0) + 1

most_used_app = max(app_counts, key=app_counts.get)

# Most distracting app
most_distracting_app = max(app_distraction, key=app_distraction.get) if app_distraction else "None"

st.write(f"Most Used App: {most_used_app}")
st.write(f"Most Distracting App: {most_distracting_app}")

# Behavior insight
if distraction_count > focus_count:
    st.warning("You are more distracted than focused.")
else:
    st.success("You are more focused than distracted.")

# Productivity insight
if productivity_score < 50:
    st.warning("Your overall productivity is low.")
else:
    st.success("Your productivity is good.")

# Recommendation
if most_distracting_app != "None":
    st.info(f"Try reducing usage of {most_distracting_app} to improve productivity.")

conn.close()