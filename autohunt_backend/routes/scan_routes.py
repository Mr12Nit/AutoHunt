from flask import Blueprint, request, jsonify
from autohunt_backend import mongo

scan_bp = Blueprint('scan_routes', __name__)

# Add a new scan
@scan_bp.route('/', methods=['POST'])
def add_scan():
    data = request.json
    if not data.get("target") or not data.get("results"):
        return jsonify({"error": "Invalid data"}), 400

    scan_id = mongo.db.scans.insert_one(data).inserted_id
    return jsonify({"message": "Scan added", "scan_id": str(scan_id)}), 201

# Get all scans
@scan_bp.route('/', methods=['GET'])
def get_scans():
    scans = list(mongo.db.scans.find({}, {'_id': False}))
    return jsonify(scans), 200
