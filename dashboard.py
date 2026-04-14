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

# ---------------- CLEAN NAME ----------------
def clean_name(app_name):
    name = app_name.lower()

    if "visual studio" in name:
        return "VS Code"

    if "notepad" in name:
        return "Notepad"

    if ".pdf" in name:
        return "PDF"

    # YouTube categories (separate bars)
    if "youtube" in name:

        # education
        if "python" in name:
            return "YT Python"
        elif "sql" in name:
            return "YT SQL"

        # food
        elif "recipe" in name or "food" in name or "fried rice" in name:
            return "YT Food"

        # movies
        elif "trailer" in name or "movie" in name:
            return "YT Movie"

        # music
        elif "song" in name or "music" in name:
            return "YT Music"

        # sports
        elif "ipl" in name or "cricket" in name:
            return "YT IPL"

        # gaming
        elif "game" in name or "gaming" in name:
            return "YT Gaming"

        else:
            return "YouTube"

    if "hill climb" in name:
        return "Hill Climb Racing"

    return app_name.split("-")[0].strip()


# ---------------- CLASSIFICATION ----------------
def classify(app_name):
    name = app_name.lower()

    focus_keywords = [
        "python tutorial","python course","python project",
        "sql tutorial","sql course","sql queries",
        "coding practice","programming tutorial","coding interview",
        "web development","app development","software development",
        "machine learning","deep learning","data science",
        "data analysis","data visualization",
        "online lecture","study material","technical tutorial",
        "debugging code","visual studio code","pycharm",
        "jupyter notebook","github","stack overflow",
        "pdf notes","research paper","documentation","study notes"
    ]

    distraction_keywords = [
        "movie trailer","full movie","film scene",
        "music video","video song","song lyrics",
        "comedy video","funny video","meme video",
        "gaming video","gameplay","live gaming",
        "hill climb racing","pubg gameplay","free fire gameplay",
        "ipl highlights","cricket match","match highlights",
        "football highlights","live match",
        "instagram reels","funny reels","short videos",
        "whatsapp status","status video",
        "cooking video","recipe video","food vlog",
        "street food","food review","restaurant review",
        "fried rice","chicken recipe","biryani recipe"
    ]

    if any(word in name for word in focus_keywords):
        return "focus"

    if any(word in name for word in distraction_keywords):
        return "distraction"

    return predict_label(name)


# ---------------- PROCESSING ----------------
focus_count = 0
distraction_count = 0

app_focus = {}
app_distraction = {}

hour_data = {}
current_streak = 0
max_streak = 0

for row in rows:
    raw_name = row[0]
    timestamp = row[1]

    if "unknown" in raw_name.lower():
        continue

    app_name = clean_name(raw_name)
    label = classify(raw_name)

    hour = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S").hour

    if hour not in hour_data:
        hour_data[hour] = {"focus": 0, "distraction": 0}

    if label == "focus":
        focus_count += 1
        app_focus[app_name] = app_focus.get(app_name, 0) + 1
        hour_data[hour]["focus"] += 1

        current_streak += 1
        max_streak = max(max_streak, current_streak)

    else:
        distraction_count += 1
        app_distraction[app_name] = app_distraction.get(app_name, 0) + 1
        hour_data[hour]["distraction"] += 1

        current_streak = 0


# ---------------- CALCULATIONS ----------------
focus_time = focus_count * 5
distraction_time = distraction_count * 5
total_time = focus_time + distraction_time

productivity_score = (focus_time / total_time) * 100 if total_time else 0


# ---------------- OVERALL STATS ----------------
st.subheader("Overall Statistics")

st.write(f"Focus Time: {focus_time} sec")
st.write(f"Distraction Time: {distraction_time} sec")
st.write(f"Total Time: {total_time} sec")
st.write(f"Productivity Score: {round(productivity_score, 2)} %")


# ---------------- PIE CHART ----------------
st.subheader("Focus vs Distraction")

fig1, ax1 = plt.subplots()
ax1.pie([focus_time, distraction_time],
        labels=["Focus", "Distraction"],
        autopct="%1.1f%%")
ax1.axis("equal")

st.pyplot(fig1)


# ---------------- LINE CHART ----------------
st.subheader("Time-based Analysis")

line_data = []
for hour in sorted(hour_data.keys()):
    line_data.append({
        "Hour": hour,
        "Focus": hour_data[hour]["focus"],
        "Distraction": hour_data[hour]["distraction"]
    })

line_df = pd.DataFrame(line_data).set_index("Hour")
st.line_chart(line_df)


# ---------------- BAR CHART ----------------
st.subheader("Top Applications (YouTube categories separated)")

all_apps = set(app_focus) | set(app_distraction)

data = []
for app in all_apps:
    data.append({
        "App": app,
        "Focus": app_focus.get(app, 0),
        "Distraction": app_distraction.get(app, 0)
    })

app_df = pd.DataFrame(data)

app_df["Total"] = app_df["Focus"] + app_df["Distraction"]
app_df = app_df.sort_values(by="Total", ascending=False).head(10)

st.bar_chart(app_df.set_index("App")[["Focus", "Distraction"]])


# ---------------- INSIGHTS ----------------
st.subheader("Personal Insights")

focus_percent = round((focus_time/total_time)*100, 2) if total_time else 0
distraction_percent = round((distraction_time/total_time)*100, 2) if total_time else 0

most_used_app = app_df.iloc[0]["App"] if not app_df.empty else "N/A"
most_distracting_app = max(app_distraction, key=app_distraction.get) if app_distraction else "N/A"
peak_hour = max(hour_data, key=lambda x: hour_data[x]["distraction"]) if hour_data else "N/A"

st.write(f"Most Used App: {most_used_app}")
st.write(f"Most Distracting App: {most_distracting_app}")
st.write(f"Focus Percentage: {focus_percent} %")
st.write(f"Distraction Percentage: {distraction_percent} %")
st.write(f"Behavior: {'Focused' if focus_count > distraction_count else 'Distracted'}")
st.write(f"Productivity: {'Good' if productivity_score > 50 else 'Low'}")
st.write(f"Peak Distraction Time: {peak_hour}:00")
st.write(f"Max Focus Streak: {max_streak}")
st.write(f"Total Sessions: {len(rows)}")

if most_distracting_app != "N/A":
    st.write(f"Recommendation: Reduce usage of {most_distracting_app}")

conn.close()