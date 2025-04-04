from flask import Blueprint, request, jsonify
from app.services.usagelog_service import UsageLogService

usagelog_bp = Blueprint("usagelog", __name__, url_prefix="/usagelogs")


@usagelog_bp.route("/", methods=["GET"])
def get_all_usagelogs():
    usagelogs = UsageLogService.get_all_usagelogs()
    return jsonify(usagelogs), 200


@usagelog_bp.route("/<int:log_id>", methods=["GET"])
def get_usagelog_by_id(log_id):
    usagelog = UsageLogService.get_usagelog_by_id(log_id)
    if usagelog:
        return jsonify(usagelog.to_dict()), 200
    return jsonify({"error": "Usage log not found"}), 404


@usagelog_bp.route("/", methods=["POST"])
def create_usagelog():
    data = request.get_json()
    result = UsageLogService.create_usagelog(data)
    if result.get("success"):
        return jsonify({"message": "Usage log created successfully"}), 201
    return jsonify({"error": result.get("error")}), 400


@usagelog_bp.route("/<int:log_id>", methods=["PUT"])
def update_usagelog(log_id):
    data = request.get_json()
    result = UsageLogService.update_usagelog(log_id, data)
    if result.get("success"):
        return jsonify({"message": "Usage log updated successfully"}), 200
    return jsonify({"error": result.get("error")}), 400


@usagelog_bp.route("/<int:log_id>", methods=["DELETE"])
def delete_usagelog(log_id):
    result = UsageLogService.delete_usagelog(log_id)
    if result.get("success"):
        return jsonify({"message": "Usage log deleted successfully"}), 200
    return jsonify({"error": result.get("error")}), 400
