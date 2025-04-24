
from flask import Blueprint, render_template, request, redirect, url_for, jsonify

from app.repositories.plan_repository import PlanRepository
from app.repositories.subscriber_repository import SubscriberRepository

from app.services.plan_service import PlanService

customer_plan_bp = Blueprint("customer_plan", __name__, url_prefix="/customer_plan")

@customer_plan_bp.route("/", methods=["GET"])
def index():
    # Redirect đến trang mobile-plans khi truy cập /customer_plan
    return redirect(url_for("customer_plan.mobile_plans"))

@customer_plan_bp.route("/mobile-plans", methods=["GET"])
def mobile_plans():
    try:
        sub_service_id = request.args.get("sub_service_id", default=3, type=int)  # Mặc định là gói 4G/5G (id=3)
        sub_services = PlanService.get_sub_services(1)  # Lấy sub-services của gói dịch vụ di động (id=1)
        plans = PlanService.get_plans_by_service_id(sub_service_id)
        return render_template("Plan_customer/list.html", plans=plans, sub_services=sub_services, selected_service_id=sub_service_id)
    except Exception as e:
        return render_template("Plan_customer/list.html", plans=[], sub_services=[], selected_service_id=3, error=str(e)), 500

@customer_plan_bp.route("/main-plans", methods=["GET"])
def main_plans():
    try:
        plans = PlanService.get_plans_by_service_id(2)  # Lấy gói cước chính (service_id=2)
        return render_template("Plan_customer/list_main.html", plans=plans)
    except Exception as e:
        return render_template("Plan_customer/list_main.html", plans=[], error=str(e)), 500

@customer_plan_bp.route("/plans/<int:plan_id>", methods=["GET"])
def plan_details(plan_id):
    try:
        plan = PlanService.get_plan_details(plan_id)
        if plan:
            return render_template("Plan_customer/detail.html", plan=plan)
        return "Plan not found", 404
    except Exception as e:

        return render_template("Plan_customer/detail.html", plan=None, error=str(e)), 500
@customer_plan_bp.route("/register-plan", methods=["POST"])
def register_plan():
    data = request.get_json()
    plan_code = data.get("plan_code")
    price = data.get("price")
    subscriber_id = data.get("subscriber_id")

    # Kiểm tra thuê bao có tồn tại không
    subscriber = SubscriberRepository.get_by_id(subscriber_id)
    if not subscriber:
        return jsonify({"success": False, "message": "Thuê bao không tồn tại!"}), 404

    # Kiểm tra số dư
    if subscriber.main_balance < price:
        return jsonify({"success": False, "message": "Số dư không đủ để đăng ký gói cước!"}), 400

    # Lấy gói cước tương ứng với code
    plan = PlanRepository.get_by_id(plan_code)
    if not plan:
        return jsonify({"success": False, "message": "Gói cước không tồn tại!"}), 404

    # (Tuỳ logic bạn có thể trừ tiền, tạo log,... ở đây nếu muốn)

    return jsonify({
        "success": True,
        "message": "Đủ điều kiện đăng ký, đang tiến hành đăng ký gói...",
        "plan_id": plan.id
    }), 200

