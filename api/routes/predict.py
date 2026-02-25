from flask import Blueprint, request, jsonify
from services.model_service import predict
from db.database import save_prediction

predict_bp = Blueprint("predict", __name__)

@predict_bp.route("/predict", methods=["POST"])
def predict_route():
    data = request.get_json(force=True)
    error_message = data.get("error_message", "").strip()
    user_count = int(data.get("user_count", 1))

    if not error_message:
        return jsonify({"error": "error_message is required"}), 400

    result = predict(error_message, user_count)
    save_prediction(
        error_message=error_message,
        user_count=user_count,
        severity=result["severity"],
        confidence=result["confidence"],
        impact_score=result["impact_score"],
    )
    return jsonify(result)
