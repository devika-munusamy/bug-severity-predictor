import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

# Load dataset
data = pd.read_csv("../data/bugs.csv")

# Features
X_text = data["error_message"]
y = data["severity"]

# Build pipeline
pipeline = Pipeline([
    ("vectorizer", TfidfVectorizer()),
    ("classifier", LogisticRegression())
])

# Train model
pipeline.fit(X_text, y)

# Save model
joblib.dump(pipeline, "model.pkl")

print("Model trained and saved successfully!")
