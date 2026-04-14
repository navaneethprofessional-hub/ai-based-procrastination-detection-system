import pandas as pd
import re
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

# ---------------- TEXT CLEANING ----------------
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    return text


# ---------------- LOAD DATA ----------------
df = pd.read_csv("training_data.csv")

# clean dataset text
df["text"] = df["text"].apply(clean_text)

# ---------------- VECTORIZATION ----------------
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(df["text"])

y = df["label"]

# ---------------- TRAIN MODEL ----------------
model = MultinomialNB()
model.fit(X, y)


# ---------------- SAVE MODEL ----------------
pickle.dump(model, open("model.pkl", "wb"))
pickle.dump(vectorizer, open("vectorizer.pkl", "wb"))


# ---------------- LOAD MODEL ----------------
model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))


# ---------------- PREDICTION FUNCTION ----------------
def predict_label(text):
    text = clean_text(text)
    text_vector = vectorizer.transform([text])
    return model.predict(text_vector)[0]