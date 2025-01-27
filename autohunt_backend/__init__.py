from flask import Flask, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS
from autohunt_backend.config import Config

# Initialize PyMongo
mongo = PyMongo()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize MongoDB and CORS
    mongo.init_app(app)
    CORS(app)

    # Health check route
    @app.route('/health', methods=['GET'])
    def health_check():
        try:
            # Check if MongoDB connection is working
            mongo.db.command('ping')
            return jsonify({"status": "success", "message": "Database connected"}), 200
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500

    # Register blueprints (API routes)
    from autohunt_backend.routes.scan_routes import scan_bp
    #from autohunt_backend.routes.exploit_routes import exploit_bp

    app.register_blueprint(scan_bp, url_prefix='/api/scans')
    #app.register_blueprint(exploit_bp, url_prefix='/api/exploits')

    return app
