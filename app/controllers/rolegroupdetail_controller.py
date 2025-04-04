from flask import Blueprint, request, jsonify
from app.services.rolegroupdetail_service import RoleGroupDetailService

role_group_detail_bp = Blueprint(
    "role_group_detail", __name__, url_prefix="/role_group_details"
)


@role_group_detail_bp.route("/", methods=["GET"])
def get_all_role_group_details():
    role_group_details = RoleGroupDetailService.get_all_role_group_details()
    return jsonify(role_group_details), 200


@role_group_detail_bp.route("/<int:role_group_id>/<int:function_id>", methods=["GET"])
def get_role_group_detail_by_id(role_group_id, function_id):
    role_group_detail = RoleGroupDetailService.get_role_group_detail_by_id(
        role_group_id, function_id
    )
    if role_group_detail:
        return jsonify(role_group_detail.to_dict()), 200
    return jsonify({"error": "Role group detail not found"}), 404


@role_group_detail_bp.route("/", methods=["POST"])
def create_role_group_detail():
    data = request.get_json()
    result = RoleGroupDetailService.create_role_group_detail(data)
    if result.get("success"):
        return jsonify({"message": "Role group detail created successfully"}), 201
    return jsonify({"error": result.get("error")}), 400


@role_group_detail_bp.route("/<int:role_group_id>/<int:function_id>", methods=["PUT"])
def update_role_group_detail(role_group_id, function_id):
    data = request.get_json()
    result = RoleGroupDetailService.update_role_group_detail(
        role_group_id, function_id, data
    )
    if result.get("success"):
        return jsonify({"message": "Role group detail updated successfully"}), 200
    return jsonify({"error": result.get("error")}), 400


@role_group_detail_bp.route(
    "/<int:role_group_id>/<int:function_id>", methods=["DELETE"]
)
def delete_role_group_detail(role_group_id, function_id):
    result = RoleGroupDetailService.delete_role_group_detail(role_group_id, function_id)
    if result.get("success"):
        return jsonify({"message": "Role group detail deleted successfully"}), 200
    return jsonify({"error": result.get("error")}), 400
