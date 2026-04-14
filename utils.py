import re
from model import predict_label

# clean raw title
def clean_app_name(app_name):
    app_name = app_name.lower()
    app_name = app_name.replace("- google chrome", "")
    app_name = app_name.replace("- chrome", "")
    app_name = re.sub(r'[^\w\s-]', '', app_name)
    return app_name.strip()


# extract meaningful phrase (intelligent cleaning)
def extract_meaning(app_name):
    app_name = clean_app_name(app_name)

    # split into parts
    parts = [p.strip() for p in app_name.split("-") if p.strip()]

    # remove common noise words
    ignore_words = ["youtube", "chrome", "official", "watch", "new"]

    clean_parts = []
    for part in parts:
        if not any(word in part for word in ignore_words):
            clean_parts.append(part)

    # choose best part (long but meaningful)
    if clean_parts:
        best = max(clean_parts, key=len)

        # remove extra spaces
        best = " ".join(best.split())

        return best

    return app_name


# hybrid classification (ML + minimal intelligence)
def classify(app_name):
    cleaned = clean_app_name(app_name)

    # slight intelligence boost (not heavy rules)
    if "github" in cleaned or "code" in cleaned:
        return "focus"

    if "game" in cleaned or "video" in cleaned:
        return "distraction"

    # fallback to ML
    return predict_label(cleaned)