from flask import Blueprint, request, jsonify
from app.services.plannetwork_service import PlanNetworkService
from flask_login import login_required
from app.utils.decorator import required

plan_network_bp = Blueprint("plan_network", __name__, url_prefix="/plan_networks")


@plan_network_bp.route("/", methods=["GET"])
def get_all_plan_networks():
    plan_networks = PlanNetworkService.get_all_plan_networks()
    print("plan_networks", plan_networks)
    if not plan_networks:
        return jsonify({"error": "No plan networks found"}), 404
    return jsonify(plan_networks), 200


@plan_network_bp.route("/<int:pn_id>", methods=["GET"])
def get_plan_network_by_id(pn_id):
    plan_network = PlanNetworkService.get_plan_network_by_id(pn_id)
    if plan_network:
        return jsonify(plan_network.to_dict()), 200
    return jsonify({"error": "Plan network not found"}), 404


@login_required
@plan_network_bp.route("/", methods=["POST"])
@required
def create_plan_network():
    data = request.get_json()
    result = PlanNetworkService.create_plan_network(data)
    if result.get("success"):
        return jsonify({"message": "Plan network created successfully"}), 201
    return jsonify({"error": result.get("error")}), 400


@login_required
@plan_network_bp.route("/<int:pn_id>", methods=["PUT"])
@required
def update_plan_network(pn_id):
    data = request.get_json()
    result = PlanNetworkService.update_plan_network(pn_id, data)
    if result.get("success"):
        return jsonify({"message": "Plan network updated successfully"}), 200
    return jsonify({"error": result.get("error")}), 400


@login_required
@plan_network_bp.route("/<int:pn_id>", methods=["DELETE"])
@required
def delete_plan_network(pn_id):
    result = PlanNetworkService.delete_plan_network(pn_id)

    if result.get("success"):
        return (
            jsonify(
                {"success": True, "message": result.get("message", "Xóa thành công")}
            ),
            200,
        )

    return (
        jsonify({"success": False, "message": result.get("error", "Xóa thất bại")}),
        400,
    )
