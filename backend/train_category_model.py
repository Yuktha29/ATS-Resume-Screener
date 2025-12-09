# Save as: backend/train_category_model.py
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib

print("Loading resume dataset...")
df = pd.read_csv('resume_dataset.csv')
df = df[['Resume_str', 'Category']].dropna()
print(f"Loaded {len(df)} resumes across {df['Category'].nunique()} categories.")

print("Training category predictor...")
vectorizer = TfidfVectorizer(max_features=5000, stop_words='english', ngram_range=(1, 2))
X = vectorizer.fit_transform(df['Resume_str'])
y = df['Category']

model = LogisticRegression(max_iter=1000, random_state=42)
model.fit(X, y)

joblib.dump(model, 'category_predictor.pkl')
joblib.dump(vectorizer, 'category_vectorizer.pkl')
print("✅ Category model saved!")