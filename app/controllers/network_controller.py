from flask import Blueprint, request, jsonify
from app.services.network_service import NetworkService

network_bp = Blueprint("network", __name__, url_prefix="/networks")


@network_bp.route("/", methods=["GET"])
def get_all_networks():
    networks = NetworkService.get_all_networks()
    return jsonify(networks), 200


@network_bp.route("/<int:network_id>", methods=["GET"])
def get_network_by_id(network_id):
    network = NetworkService.get_network_by_id(network_id)
    if network:
        return jsonify(network.to_dict()), 200
    return jsonify({"error": "Network not found"}), 404


@network_bp.route("/", methods=["POST"])
def create_network():
    data = request.get_json()
    result = NetworkService.create_network(data)
    if result.get("success"):
        return jsonify({"message": "Network created successfully"}), 201
    return jsonify({"error": result.get("error")}), 400


@network_bp.route("/<int:network_id>", methods=["PUT"])
def update_network(network_id):
    data = request.get_json()
    result = NetworkService.update_network(network_id, data)
    if result.get("success"):
        return jsonify({"message": "Network updated successfully"}), 200
    return jsonify({"error": result.get("error")}), 400


@network_bp.route("/<int:network_id>", methods=["DELETE"])
def delete_network(network_id):
    result = NetworkService.delete_network(network_id)
    if result.get("success"):
        return jsonify({"message": "Network deleted successfully"}), 200
    return jsonify({"error": result.get("error")}), 400
