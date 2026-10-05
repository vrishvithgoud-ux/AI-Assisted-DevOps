from flask import Blueprint, jsonify


services_bp = Blueprint("services", __name__)


services = [
    {
        "id": 1,
        "name": "payment-service",
        "status": "running",
        "description": "Handles payment processing",
    },
    {
        "id": 2,
        "name": "user-service",
        "status": "running",
        "description": "Handles user management",
    },
]


@services_bp.get("/services")
def list_services():
    return jsonify(services)
