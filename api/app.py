from flask import Flask
from flask_cors import CORS
from extensions import socketio
from db.database import init_db
from routes.predict import predict_bp
from routes.history import history_bp
from routes.anomaly import anomaly_bp
from routes.receiver import receiver_bp

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}})

    # Initialise SQLite on startup
    init_db()

    # Init SocketIO with app
    socketio.init_app(app)

    # Register blueprints
    app.register_blueprint(predict_bp)
    app.register_blueprint(history_bp)
    app.register_blueprint(anomaly_bp)
    app.register_blueprint(receiver_bp)

    return app

if __name__ == "__main__":
    app = create_app()
    socketio.run(app, debug=True, port=5000)