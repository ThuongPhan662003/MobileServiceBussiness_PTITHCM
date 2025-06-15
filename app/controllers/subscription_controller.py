from decimal import Decimal

from flask import Blueprint, request, jsonify

from app.repositories.plan_repository import PlanRepository
from app.repositories.subscriber_repository import SubscriberRepository
from app.services.subscription_service import SubscriptionService
from flask_login import login_required
from app.utils.decorator import required

subscription_bp = Blueprint("subscription", __name__, url_prefix="/subscriptions")


@login_required
@subscription_bp.route("/", methods=["GET"])
@required
def get_all_subscriptions():
    subscriptions = SubscriptionService.get_all_subscriptions()
    return jsonify(subscriptions), 200


@login_required
@subscription_bp.route("/<int:subscription_id>", methods=["GET"])
@required
def get_subscription_by_id(subscription_id):
    subscription = SubscriptionService.get_subscription_by_id(subscription_id)
    if subscription:
        return jsonify(subscription.to_dict()), 200
    return jsonify({"error": "Subscription not found"}), 404


@login_required
@subscription_bp.route("/<int:subscriber_id>/<int:plan_id>", methods=["POST"])
# @required
def create_subscription(subscriber_id, plan_id):
    confirm_override = request.json.get("confirm_override", False)
    result = SubscriptionService.create_subscription(subscriber_id, plan_id, confirm_override)
    if result.get("success"):
        return jsonify(result), 201
    return jsonify({"error": result.get("error")}), 400

@login_required
@subscription_bp.route("/<int:subscription_id>", methods=["PUT"])
@required
def update_subscription(subscription_id):
    data = request.get_json()
    result = SubscriptionService.update_subscription(subscription_id, data)
    if result.get("success"):
        return jsonify({"message": "Subscription updated successfully"}), 200
    return jsonify({"error": result.get("error")}), 400


@login_required
@subscription_bp.route("/<int:subscription_id>", methods=["DELETE"])
@required
def delete_subscription(subscription_id):
    result = SubscriptionService.delete_subscription(subscription_id)
    if isinstance(result, dict) and result.get("success"):
        return jsonify({"success": True, "message": result.get("message")}), 200
    else:
        return (
            jsonify(
                {
                    "success": False,
                    "message": result.get("message", "Hủy subscription thất bại!"),
                }
            ),
            400,
        )


# Endpoint đăng ký gói cước qua tài khoản gốc


@login_required
@subscription_bp.route("/deduct/<int:subscriber_id>/<int:plan_id>", methods=["POST"])
@required
def deduct_balance(subscriber_id, plan_id):
    try:
        # Lấy thông tin gói cước
        plan = PlanRepository.get_by_id(plan_id)
        if not plan:
            return jsonify({"error": "Không tìm thấy gói cước."}), 404

        # Lấy thông tin thuê bao để trừ tiền tài khoản chính
        subscriber = SubscriberRepository.get_by_id(subscriber_id)
        if not subscriber:
            return jsonify({"error": "Không tìm thấy thuê bao."}), 404

        # Kiểm tra số dư tài khoản chính
        if subscriber.main_balance < plan.price:
            return jsonify({"error": "Số dư tài khoản không đủ để thanh toán."}), 400

        # Trừ tiền tài khoản chính
        plan_price = Decimal(str(plan.price))
        subscriber.main_balance -= plan_price
        SubscriberRepository.update(subscriber.id, subscriber)

        return (
            jsonify({"success": True, "message": "Trừ tiền tài khoản thành công."}),
            200,
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@login_required
@subscription_bp.route("/qr/<int:subscriber_id>/<int:plan_id>", methods=["POST"])
# @required
def create_subscription1(subscriber_id, plan_id):
    confirm_override = request.json.get("confirm_override", False)
    result = SubscriptionService.create_subscription1(subscriber_id, plan_id, confirm_override)
    if result.get("success"):
        return jsonify(result), 201
    return jsonify({"error": result.get("error")}), 400