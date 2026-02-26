from flask import Blueprint, jsonify
from services.anomaly_detector import get_anomaly_status

anomaly_bp = Blueprint("anomaly", __name__)


@anomaly_bp.route("/anomaly-status", methods=["GET"])
def anomaly_status_route():
    status = get_anomaly_status()
    return jsonify(status)
