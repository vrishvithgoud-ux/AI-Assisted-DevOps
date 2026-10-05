from flask import Blueprint, jsonify


services_bp = Blueprint("services", __name__)


@services_bp.get("/services")
def list_services():
    services = [
        {"id": 1, "name": "incident-api", "status": "healthy"},
        {"id": 2, "name": "notification-service", "status": "healthy"},
    ]
    return jsonify(services)
