import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler
import numpy as np

# Load dataset
data = pd.read_csv("../data/bugs.csv")

X = data[["error_message", "user_count"]]
y = data["severity"]

# ColumnTransformer: TF-IDF on text + StandardScaler on numeric
preprocessor = ColumnTransformer(transformers=[
    ("tfidf", TfidfVectorizer(), "error_message"),
    ("scaler", StandardScaler(), ["user_count"]),
])

# Full pipeline
pipeline = Pipeline([
    ("preprocessor", preprocessor),
    ("classifier", LogisticRegression(max_iter=1000)),
])

# Train
pipeline.fit(X, y)

# Save
joblib.dump(pipeline, "model.pkl")
print("✅ Model trained and saved — features: error_message (TF-IDF) + user_count (scaled)")
