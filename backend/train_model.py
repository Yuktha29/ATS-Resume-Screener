# backend/train_model.py
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import joblib

print("Loading resume dataset...")
df = pd.read_csv('resume_dataset.csv')

# Keep only needed columns
df = df[['Resume_str', 'Category']].dropna()
print(f"Loaded {len(df)} resumes across {df['Category'].nunique()} categories.")

# Vectorize resume text
print("Vectorizing text with TF-IDF...")
vectorizer = TfidfVectorizer(
    max_features=3000,
    stop_words='english',
    lowercase=True,
    ngram_range=(1, 2)  # unigrams + bigrams
)
X = vectorizer.fit_transform(df['Resume_str'])
y = df['Category']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Train Logistic Regression (fast + interpretable)
print("Training Logistic Regression model...")
model = LogisticRegression(max_iter=1000, random_state=42)
model.fit(X_train, y_train)

# Evaluate
train_acc = model.score(X_train, y_train)
test_acc = model.score(X_test, y_test)
print(f"Train Accuracy: {train_acc:.2%}")
print(f"Test Accuracy:  {test_acc:.2%}")

# Save model & vectorizer for Flask backend
joblib.dump(model, 'resume_model.pkl')
joblib.dump(vectorizer, 'vectorizer.pkl')
print("✅ Model saved as 'resume_model.pkl'")
print("✅ Vectorizer saved as 'vectorizer.pkl'")