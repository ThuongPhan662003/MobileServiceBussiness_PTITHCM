from flask import Blueprint, request, jsonify
from flask_login import login_required
from app.services.plandetail_service import PlanDetailService

plan_detail_bp = Blueprint("plan_detail", __name__, url_prefix="/plan_details")


@plan_detail_bp.route("/", methods=["GET"])
@login_required
def get_all_plan_details():
    plan_details = PlanDetailService.get_all_plan_details()
    return jsonify(plan_details), 200


@plan_detail_bp.route("/<int:plan_id>", methods=["GET"])
@login_required
def get_plan_detail_by_id(plan_id):
    plan_detail = PlanDetailService.get_plan_detail_by_id(plan_id)
    if plan_detail:
        return jsonify(plan_detail.to_dict()), 200
    return jsonify({"error": "Plan detail not found"}), 404


@plan_detail_bp.route("/", methods=["POST"])
@login_required
def create_plan_detail():
    data = request.get_json()
    result = PlanDetailService.create_plan_detail(data)
    if result.get("success"):
        return jsonify({"message": "Plan detail created successfully"}), 201
    return jsonify({"error": result.get("error")}), 400


@plan_detail_bp.route("/<int:plan_id>", methods=["PUT"])
@login_required
def update_plan_detail(plan_id):
    data = request.get_json()
    result = PlanDetailService.update_plan_detail(plan_id, data)
    if result.get("success"):
        return jsonify({"message": "Plan detail updated successfully"}), 200
    return jsonify({"error": result.get("error")}), 400


@plan_detail_bp.route("/<int:plan_id>", methods=["DELETE"])
@login_required
def delete_plan_detail(plan_id):
    result = PlanDetailService.delete_plan_detail(plan_id)
    if result.get("success"):
        return jsonify({"message": "Plan detail deleted successfully"}), 200
    return jsonify({"error": result.get("error")}), 400
