from flask import Blueprint, request, jsonify
from services.model_service import predict
from services.root_cause_engine import analyze_error
from db.database import save_prediction
import datetime

receiver_bp = Blueprint("receiver", __name__)

@receiver_bp.route("/api/v1/receive", methods=["POST"])
def receive_event():
    """
    Endpoint for external applications to send live error data.
    Expected JSON: { "error_message": "...", "user_count": 1, "app_source": "external-app" }
    """
    from extensions import socketio  # Avoid circular import

    data = request.get_json(force=True)
    error_message = data.get("error_message", "").strip()
    user_count = int(data.get("user_count", 1))
    app_source = data.get("app_source", "unknown")

    if not error_message:
        return jsonify({"status": "error", "message": "error_message is required"}), 400

    # ML severity prediction
    result = predict(error_message, user_count)

    # Rule-based root cause analysis
    analysis = analyze_error(error_message)

    # Persist to DB
    prediction_id = save_prediction(
        error_message=f"[{app_source}] {error_message}",
        user_count=user_count,
        severity=result["severity"],
        confidence=result["confidence"],
        impact_score=result["impact_score"],
        error_category=analysis["category"],
    )

    # Broadcast to all clients for "Live Monitoring"
    live_event = {
        "id": prediction_id,
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "error_message": f"[{app_source}] {error_message}",
        "user_count": user_count,
        "predicted_severity": result["severity"],
        "confidence": result["confidence"],
        "impact_score": result["impact_score"],
        "error_category": analysis["category"]
    }

    socketio.emit("new_bug", live_event)

    return jsonify({
        "status": "success",
        "received": {
            "error_message": error_message,
            "severity": result["severity"],
            "category": analysis["category"],
            "impact_score": result["impact_score"]
        }
    }), 201
