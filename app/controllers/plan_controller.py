from flask import Blueprint, request, jsonify
from app.services.plan_service import PlanService

plan_bp = Blueprint("plan", __name__, url_prefix="/plans")


@plan_bp.route("/", methods=["GET"])
def get_all_plans():
    plans = PlanService.get_all_plans()
    return jsonify(plans), 200


@plan_bp.route("/<int:plan_id>", methods=["GET"])
def get_plan_by_id(plan_id):
    plan = PlanService.get_plan_by_id(plan_id)
    if plan:
        return jsonify(plan.to_dict()), 200
    return jsonify({"error": "Plan not found"}), 404


@plan_bp.route("/", methods=["POST"])
def create_plan():
    data = request.get_json()
    result = PlanService.create_plan(data)
    if result.get("success"):
        return jsonify({"message": "Plan created successfully"}), 201
    return jsonify({"error": result.get("error")}), 400


@plan_bp.route("/<int:plan_id>", methods=["PUT"])
def update_plan(plan_id):
    data = request.get_json()
    result = PlanService.update_plan(plan_id, data)
    if result.get("success"):
        return jsonify({"message": "Plan updated successfully"}), 200
    return jsonify({"error": result.get("error")}), 400


@plan_bp.route("/<int:plan_id>", methods=["DELETE"])
def delete_plan(plan_id):
    result = PlanService.delete_plan(plan_id)
    if result.get("success"):
        return jsonify({"message": "Plan deleted successfully"}), 200
    return jsonify({"error": result.get("error")}), 400
