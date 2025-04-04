from flask import Blueprint, request, jsonify
from app.services.staff_service import StaffService

staff_bp = Blueprint("staff", __name__, url_prefix="/staffs")


@staff_bp.route("/", methods=["GET"])
def get_all_staffs():
    staffs = StaffService.get_all_staffs()
    return jsonify(staffs), 200


@staff_bp.route("/<int:staff_id>", methods=["GET"])
def get_staff_by_id(staff_id):
    staff = StaffService.get_staff_by_id(staff_id)
    if staff:
        return jsonify(staff.to_dict()), 200
    return jsonify({"error": "Staff not found"}), 404


@staff_bp.route("/", methods=["POST"])
def create_staff():
    data = request.get_json()
    result = StaffService.create_staff(data)
    if result.get("success"):
        return jsonify({"message": "Staff created successfully"}), 201
    return jsonify({"error": result.get("error")}), 400


@staff_bp.route("/<int:staff_id>", methods=["PUT"])
def update_staff(staff_id):
    data = request.get_json()
    result = StaffService.update_staff(staff_id, data)
    if result.get("success"):
        return jsonify({"message": "Staff updated successfully"}), 200
    return jsonify({"error": result.get("error")}), 400


@staff_bp.route("/<int:staff_id>", methods=["DELETE"])
def delete_staff(staff_id):
    result = StaffService.delete_staff(staff_id)
    if result.get("success"):
        return jsonify({"message": "Staff deleted successfully"}), 200
    return jsonify({"error": result.get("error")}), 400
