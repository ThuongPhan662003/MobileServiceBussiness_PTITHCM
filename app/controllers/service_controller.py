from flask import Blueprint, request, jsonify
from app.services.service_service import ServiceService

service_bp = Blueprint("service", __name__, url_prefix="/services")


@service_bp.route("/", methods=["GET"])
def get_all_services():
    services = ServiceService.get_all_services()
    return jsonify(services), 200


@service_bp.route("/<int:service_id>", methods=["GET"])
def get_service_by_id(service_id):
    service = ServiceService.get_service_by_id(service_id)
    if service:
        return jsonify(service.to_dict()), 200
    return jsonify({"error": "Service not found"}), 404


@service_bp.route("/", methods=["POST"])
def create_service():
    data = request.get_json()
    result = ServiceService.create_service(data)
    if result.get("success"):
        return jsonify({"message": "Service created successfully"}), 201
    return jsonify({"error": result.get("error")}), 400


@service_bp.route("/<int:service_id>", methods=["PUT"])
def update_service(service_id):
    data = request.get_json()
    result = ServiceService.update_service(service_id, data)
    if result.get("success"):
        return jsonify({"message": "Service updated successfully"}), 200
    return jsonify({"error": result.get("error")}), 400


@service_bp.route("/<int:service_id>", methods=["DELETE"])
def delete_service(service_id):
    result = ServiceService.delete_service(service_id)
    if result.get("success"):
        return jsonify({"message": "Service deleted successfully"}), 200
    return jsonify({"error": result.get("error")}), 400
