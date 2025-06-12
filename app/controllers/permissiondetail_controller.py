from flask import Blueprint, request, jsonify
from app.services.permissiondetail_service import PermissionDetailService
from flask_login import login_required
from app.utils.decorator import required

permission_bp = Blueprint("permission", __name__, url_prefix="/permission_details")


@login_required
@permission_bp.route("/", methods=["GET"])
@required
def get_all_permissions():
    permissions = PermissionDetailService.get_all_permission_details()
    return jsonify(permissions), 200


@login_required
@permission_bp.route("/<int:role_group_id>/<int:account_id>", methods=["GET"])
@required
def get_permission_by_id(role_group_id, account_id):
    permission = PermissionDetailService.get_permission_detail_by_id(
        role_group_id, account_id
    )
    if permission:
        return jsonify(permission.to_dict()), 200
    return jsonify({"error": "Permission not found"}), 404


@login_required
@permission_bp.route("/", methods=["POST"])
@required
def create_permission():
    data = request.get_json()
    result = PermissionDetailService.create_permission_detail(data)
    if result.get("success"):
        return jsonify({"message": "Permission created successfully"}), 201
    return jsonify({"error": result.get("error")}), 400


@login_required
@permission_bp.route("/<int:role_group_id>/<int:account_id>", methods=["DELETE"])
@required
def delete_permission(role_group_id, account_id):
    result = PermissionDetailService.delete_permission_detail(role_group_id, account_id)
    if result.get("success"):
        return jsonify({"message": "Permission deleted successfully"}), 200
    return jsonify({"error": result.get("error")}), 400
