from flask import Blueprint, request, jsonify
from services.model_service import predict
from services.root_cause_engine import analyze_error
from db.database import save_prediction
import datetime

predict_bp = Blueprint("predict", __name__)


@predict_bp.route("/predict", methods=["POST"])
def predict_route():
    from extensions import socketio

    data = request.get_json(force=True)
    error_message = data.get("error_message", "").strip()
    user_count = int(data.get("user_count", 1))

    if not error_message:
        return jsonify({"error": "error_message is required"}), 400

    # ML severity prediction
    result = predict(error_message, user_count)

    # Rule-based root cause analysis
    analysis = analyze_error(error_message)

    # Persist to DB
    prediction_id = save_prediction(
        error_message=error_message,
        user_count=user_count,
        severity=result["severity"],
        confidence=result["confidence"],
        impact_score=result["impact_score"],
        error_category=analysis["category"],
        root_cause=analysis["root_cause"],
        suggested_fix=analysis["suggested_fix"],
    )

    # Broadcast for Live Monitoring
    live_event = {
        "id": prediction_id,
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "error_message": error_message,
        "user_count": user_count,
        "predicted_severity": result["severity"],
        "confidence": result["confidence"],
        "impact_score": result["impact_score"],
        "error_category": analysis["category"],
        "root_cause": analysis["root_cause"],
        "suggested_fix": analysis["suggested_fix"],
    }
    socketio.emit("new_bug", live_event)

    return jsonify({**result, **analysis})
