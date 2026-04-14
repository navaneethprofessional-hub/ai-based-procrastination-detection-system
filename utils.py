import re

# ---------------- CLEAN APP NAME ----------------
def clean_app_name(app_name):
    app_name = app_name.lower()

    # remove browser text
    app_name = app_name.replace("- google chrome", "")
    app_name = app_name.replace("- chrome", "")
    app_name = app_name.replace("youtube -", "")
    app_name = app_name.strip()

    return app_name


# ---------------- EXTRACT MEANINGFUL NAME ----------------
def extract_meaning(app_name):
    app_name = clean_app_name(app_name)

    # YouTube handling
    if "youtube" in app_name:
        parts = app_name.split("-")

        # try to extract channel name (last part)
        if len(parts) > 1:
            return parts[-1].strip()

        return "youtube"

    # GitHub
    if "github" in app_name:
        return "github"

    # SQL
    if "sql" in app_name:
        return "sql"

    # Python
    if "python" in app_name:
        return "python"

    # Gaming
    gaming_keywords = ["free fire", "pubg", "game", "gaming"]
    if any(word in app_name for word in gaming_keywords):
        return "gaming"

    # Movies
    movie_keywords = ["movie", "trailer"]
    if any(word in app_name for word in movie_keywords):
        return "movie"

    # default → first meaningful word
    return app_name.split()[0]


# ---------------- CLASSIFICATION ----------------
def classify(app_name, predict_label):
    name = app_name.lower()

    focus_keywords = [
        "visual studio",
        "code",
        "github",
        "sql",
        "python",
        "notebook",
        "pycharm",
        "terminal"
    ]

    distraction_keywords = [
        "youtube",
        "gaming",
        "movie",
        "instagram",
        "reel"
    ]

    if any(k in name for k in focus_keywords):
        return "focus"

    if any(k in name for k in distraction_keywords):
        return "distraction"

    return predict_label(name)