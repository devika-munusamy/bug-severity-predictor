import joblib
import os
import math

MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "model", "model.pkl")

_model = None

def load_model():
    global _model
    if _model is None:
        _model = joblib.load(MODEL_PATH)
    return _model

def predict(error_message: str, user_count: int) -> dict:
    model = load_model()
    import pandas as pd
    X = pd.DataFrame([{"error_message": error_message, "user_count": user_count}])
    severity = model.predict(X)[0]
    confidence = float(model.predict_proba(X).max())
    impact_score = compute_impact_score(severity, confidence, user_count)
    return {
        "severity": severity,
        "confidence": confidence,
        "impact_score": impact_score,
    }

def compute_impact_score(severity: str, confidence: float, user_count: int) -> float:
    """
    Weighted formula:
        impact = severity_weight * confidence * log1p(user_count)
    severity_weight: High=3, Medium=2, Low=1
    """
    weight = {"High": 3, "Medium": 2, "Low": 1}
    w = weight.get(severity, 1)
    return round(w * confidence * math.log1p(user_count), 4)
