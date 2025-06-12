from flask import Blueprint, flash, redirect, render_template, request, jsonify, url_for
import paypalrestsdk
from flask_login import login_required
from app.utils.decorator import required
from app.repositories.plan_repository import PlanRepository
from app.repositories.subscriber_repository import SubscriberRepository
from app.repositories.subscription_repository import SubscriptionRepository
from app.services.payment_service import PaymentService
from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify
from datetime import datetime

payment_bp = Blueprint("payment_bp", __name__, url_prefix="/payments")


@login_required
@payment_bp.route("/getallpays", methods=["GET"])
@required
def get_all_payments():
    payments = PaymentService.get_all_payments()
    return jsonify(payments), 200


@login_required
@payment_bp.route("/<int:payment_id>", methods=["GET"])
@required
def get_payment_by_id(payment_id):
    payment = PaymentService.get_payment_by_id(payment_id)
    if payment:
        return jsonify(payment.to_dict()), 200
    return jsonify({"error": "Payment not found"}), 404


@login_required
@payment_bp.route("/<int:subscriber_id>/<int:plan_id>", methods=["POST"])
@required
def create_payment(subscriber_id, plan_id):
    try:
        subscription_id = (
            SubscriptionRepository.get_subscription_by_subscriber_and_plan(
                subscriber_id, plan_id
            )
        )
        subscriber = SubscriberRepository.get_by_id(subscriber_id)
        if not subscriber:
            print("Không tìm thấy thuê bao.")
            return jsonify({"error": "Không tìm thấy thuê bao."}), 404

        plan = PlanRepository.get_by_id(plan_id)
        if not plan:
            print("Không tìm thấy gói cước.")
            return jsonify({"error": "Không tìm thấy gói cước."}), 404

        # Kiểm tra loại thuê bao (trả trước hoặc không)
        if subscriber.subscriber_type == "TRATRUOC":
            payment_data = {
                "subscription_id": subscription_id,
                "payment_date": datetime.now(),
                "total_amount": float(plan.price),
                "payment_method": request.json.get("payment_method", "QRcode"),
                "is_paid": True,
                "due_date": datetime.now(),  # Đảm bảo là đối tượng datetime
            }

        else:
            current_year = datetime.now().year
            current_month = datetime.now().month
            if current_month == 12:
                due_date = datetime(
                    current_year + 1, 1, 1, 0, 0, 0
                )  # 00:00 ngày 1 tháng 1 của năm tiếp theo
            else:
                due_date = datetime(
                    current_year, current_month + 1, 1, 0, 0, 0
                )  # 00:00 ngày 1 tháng sau

            payment_data = {
                "subscription_id": subscription_id,
                "payment_date": datetime.now(),
                "total_amount": float(plan.price),
                "payment_method": "QRcode",
                "is_paid": False,
                "due_date": due_date,  # Đảm bảo là đối tượng datetime
            }

        print("📦 payment_data:", payment_data)

        result = PaymentService.create_payment(payment_data)
        print("📥 Kết quả từ create_payment:", result)

        if result.get("success"):
            # Trả về id_payment trong kết quả
            return (
                jsonify(
                    {
                        "message": "Tạo thanh toán thành công.",
                        "id_payment": result.get("id_payment"),
                    }
                ),
                201,
            )
        return jsonify({"error": result.get("error")}), 400

    except Exception as e:
        print("🔥 Lỗi trong create_payment:", str(e))
        return jsonify({"error": str(e)}), 500


@login_required
@payment_bp.route("/<int:payment_id>", methods=["PUT"])
@required
def update_payment(payment_id):
    data = request.get_json()
    result = PaymentService.update_payment(payment_id, data)
    if result.get("success"):
        return jsonify({"message": "Payment updated successfully"}), 200
    return jsonify({"error": result.get("error")}), 400


@login_required
@payment_bp.route("/<int:payment_id>", methods=["DELETE"])
@required
def delete_payment(payment_id):
    result = PaymentService.delete_payment(payment_id)
    if result.get("success"):
        return jsonify({"message": "Payment deleted successfully"}), 200
    return jsonify({"error": result.get("error")}), 400
