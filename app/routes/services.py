from flask import Blueprint, current_app, jsonify, request
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from ..models.service import Service


services_bp = Blueprint("services", __name__)


@services_bp.get("/services")
def list_services():
    session_factory = current_app.extensions["sqlalchemy_session_factory"]

    with session_factory() as session:
        services = session.scalars(select(Service)).all()
        result = [
            {
                "id": service.id,
                "name": service.name,
                "status": service.status,
                "description": service.description,
                "created_at": service.created_at.isoformat(),
                "updated_at": service.updated_at.isoformat(),
            }
            for service in services
        ]

    return jsonify(result)


@services_bp.post("/services")
def create_service():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify(error="Request body must be a JSON object."), 400

    name = data.get("name")
    status = data.get("status")
    description = data.get("description")
    if not isinstance(name, str) or not name.strip():
        return jsonify(error="'name' is required and must be a non-empty string."), 400
    if not isinstance(status, str) or not status.strip():
        return jsonify(error="'status' is required and must be a non-empty string."), 400
    if description is not None and not isinstance(description, str):
        return jsonify(error="'description' must be a string or null."), 400

    session_factory = current_app.extensions["sqlalchemy_session_factory"]
    with session_factory() as session:
        try:
            existing = session.scalar(select(Service).where(Service.name == name))
            if existing is not None:
                return jsonify(error="A service with that name already exists."), 409

            service = Service(name=name, status=status, description=description)
            session.add(service)
            session.commit()
            session.refresh(service)
        except IntegrityError:
            session.rollback()
            try:
                duplicate = session.scalar(select(Service.id).where(Service.name == name))
            except SQLAlchemyError:
                session.rollback()
                return jsonify(error="A database error occurred."), 500

            if duplicate is not None:
                return jsonify(error="A service with that name already exists."), 409
            return jsonify(error="A database error occurred."), 500
        except SQLAlchemyError:
            session.rollback()
            return jsonify(error="A database error occurred."), 500

        result = {
            "id": service.id,
            "name": service.name,
            "status": service.status,
            "description": service.description,
            "created_at": service.created_at.isoformat(),
            "updated_at": service.updated_at.isoformat(),
        }

    return jsonify(result), 201
