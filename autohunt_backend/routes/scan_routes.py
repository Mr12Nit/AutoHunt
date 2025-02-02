from flask import Blueprint, request, jsonify
from autohunt_backend import mongo
# Import the nmap_handler.scan_ports function
import autohunt_backend.services.nmap_handler as NmapHandler 

scan_bp = Blueprint('scan_routes', __name__)

@scan_bp.route('/', methods=['POST'])
def add_scan():
    data = request.json
    target = data.get('target')
    scan_name = data.get('scanName')

    if not target:
        return jsonify({"error": "No target provided"}), 400

    try:
        # 1. Run the Nmap scan
        scan_handlert = NmapHandler()
        results = scan_handlert.scan_ports(target)

        # 2. Build the document you want to store
        scan_doc = {
            "scan_name": scan_name,
            "target": target,
            "results": results
        }

        # 3. Insert into Mongo
        scan_id = mongo.db.scans.insert_one(scan_doc).inserted_id

        # 4. Return success
        return jsonify({
            "message": "Scan added",
            "scan_id": str(scan_id),
            "results": results  # optional to return
        }), 201

    except Exception as e:
        # If scan_ports raises any exception or something goes wrong
        return jsonify({"error": str(e)}), 500

@scan_bp.route('/', methods=['GET'])
def get_scans():
    scans = list(mongo.db.scans.find({}, {'_id': False}))
    return jsonify(scans), 200
