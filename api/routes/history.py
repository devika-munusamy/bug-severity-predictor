from flask import Blueprint, jsonify
from db.database import get_history

history_bp = Blueprint("history", __name__)

@history_bp.route("/history", methods=["GET"])
def history_route():
    records = get_history()
    return jsonify(records)
