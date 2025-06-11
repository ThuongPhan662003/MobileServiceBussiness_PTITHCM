from flask import Blueprint, render_template, request, jsonify
from app.services.network_service import NetworkService
from flask_login import login_required
from app.utils.decorator import required

network_bp = Blueprint("network", __name__, url_prefix="/networks")


@login_required
@network_bp.route("/", methods=["GET"])
@required
def index():
    return render_template("networks/networks.html")


@login_required
@network_bp.route("/get-all", methods=["GET"])
@required
def get_all_networks():
    networks = NetworkService.get_all_networks()
    return jsonify(networks), 200


@login_required
@network_bp.route("/<int:network_id>", methods=["GET"])
@required
def get_network_by_id(network_id):
    network = NetworkService.get_network_by_id(network_id)
    if network:
        return jsonify(network.to_dict()), 200
    return (
        jsonify({"success": False, "error": True, "message": "Network not found"}),
        404,
    )


@login_required
@network_bp.route("/", methods=["POST"])
@required
def create_network():
    data = request.get_json()
    result = NetworkService.create_network(data)
    if result.get("success"):
        return (
            jsonify({"success": True, "message": "Network created successfully"}),
            201,
        )
    return jsonify(result), 400  # result đã có error + message


@login_required
@network_bp.route("/<int:network_id>", methods=["PUT"])
@required
def update_network(network_id):
    data = request.get_json()
    result = NetworkService.update_network(network_id, data)
    if result.get("success"):
        return (
            jsonify({"success": True, "message": "Network updated successfully"}),
            200,
        )
    return jsonify(result), 400


@login_required
@network_bp.route("/<int:network_id>", methods=["DELETE"])
@required
def delete_network(network_id):
    result = NetworkService.delete_network(network_id)

    if result.get("success"):
        return (
            jsonify(
                {
                    "success": True,
                    "message": result.get("message", "Xóa mạng thành công"),
                }
            ),
            200,
        )

    return (
        jsonify(
            {"success": False, "message": result.get("message", "Xóa mạng thất bại")}
        ),
        400,
    )
