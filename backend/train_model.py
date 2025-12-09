# backend/train_model.py
import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

print("Loading training pairs...")
df = pd.read_csv('training_pairs.csv')
print(f"Loaded {len(df)} pairs. Positive samples: {df['label'].sum()} ({df['label'].mean():.1%})")

# Combine resume + job description
df['combined_text'] = df['resume_text'].fillna('') + " [SEP] " + df['jd_text'].fillna('')

# Vectorize
print("Vectorizing text with TF-IDF...")
vectorizer = TfidfVectorizer(
    max_features=5000,
    stop_words='english',
    lowercase=True,
    ngram_range=(1, 2),
    min_df=2
)
X = vectorizer.fit_transform(df['combined_text'])
y = df['label']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Train model
print("Training Logistic Regression model...")
model = LogisticRegression(max_iter=1000, random_state=42)
model.fit(X_train, y_train)

# Evaluate
train_acc = model.score(X_train, y_train)
test_acc = model.score(X_test, y_test)
print(f"Train Accuracy: {train_acc:.2%}")
print(f"Test Accuracy:  {test_acc:.2%}")

# Optional: detailed report
print("\nClassification Report:")
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

# Save
joblib.dump(model, 'resume_matcher.pkl')
joblib.dump(vectorizer, 'pair_vectorizer.pkl')
print("\nModel saved as 'resume_matcher.pkl'")
print("Vectorizer saved as 'pair_vectorizer.pkl'")