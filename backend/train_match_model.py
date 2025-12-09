import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import joblib

df = pd.read_csv("training_pairs.csv")
df["combined"] = df["resume_text"] + " " + df["jd_text"]

vectorizer = TfidfVectorizer(max_features=5000, stop_words="english")
X = vectorizer.fit_transform(df["combined"])
y = df["label"]

X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=0.2)

model = LogisticRegression(max_iter=3000)
model.fit(X_train, y_train)

preds = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, preds))

joblib.dump(model, "match_model.pkl")
joblib.dump(vectorizer, "match_vectorizer.pkl")
print("Saved match_model.pkl + match_vectorizer.pkl")