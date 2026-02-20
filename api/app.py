from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib

app = Flask(__name__)

# ✅ Enable CORS for all routes
CORS(app, resources={r"/*": {"origins": "*"}})

model = joblib.load("../model/model.pkl")

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    error_message = data["error_message"]

    prediction = model.predict([error_message])[0]
    probability = model.predict_proba([error_message]).max()

    return jsonify({
        "severity": prediction,
        "confidence": float(probability)
    })

if __name__ == "__main__":
    app.run(debug=True)