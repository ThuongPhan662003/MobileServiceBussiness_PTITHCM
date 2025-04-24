from flask import Blueprint, flash, redirect, render_template, request, jsonify, url_for
import paypalrestsdk

from app.repositories.plan_repository import PlanRepository
from app.repositories.subscriber_repository import SubscriberRepository
from app.repositories.subscription_repository import SubscriptionRepository
from app.services.payment_service import PaymentService

payment_bp = Blueprint("payment_bp", __name__, url_prefix="/payments")




@payment_bp.route("/getallpays", methods=["GET"])
def get_all_payments():
    payments = PaymentService.get_all_payments()
    return jsonify(payments), 200


@payment_bp.route("/<int:payment_id>", methods=["GET"])
def get_payment_by_id(payment_id):
    payment = PaymentService.get_payment_by_id(payment_id)
    if payment:
        return jsonify(payment.to_dict()), 200
    return jsonify({"error": "Payment not found"}), 404


from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify
from datetime import datetime

@payment_bp.route("/<int:subscriber_id>/<int:plan_id>", methods=["POST"])
def create_payment(subscriber_id, plan_id):
    try:
        subscription_id = SubscriptionRepository.get_subscription_by_subscriber_and_plan(subscriber_id,plan_id)
        subscriber = SubscriberRepository.get_by_id(subscriber_id)
        if not subscriber:
            print("Không tìm thấy thuê bao.")
            return jsonify({"error": "Không tìm thấy thuê bao."}), 404

        plan = PlanRepository.get_by_id(plan_id)
        if not plan:
            print("Không tìm thấy gói cước.")
            return jsonify({"error": "Không tìm thấy gói cước."}), 404

        # Chuyển đổi due_date sang đối tượng datetime
        due_date_str = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")  # Chuỗi ngày
        due_date = datetime.strptime(due_date_str, "%Y-%m-%d")  # Chuyển thành datetime object

        payment_data = {
            "subscription_id":subscription_id,
            "payment_date": datetime.now(),
            "total_amount": float(plan.price),
            "payment_method": request.json.get("payment_method", "qr"),
            "is_paid": False,
            "due_date": due_date,  # Đảm bảo là đối tượng datetime
        }

        print("📦 payment_data:", payment_data)

        result = PaymentService.create_payment(payment_data)
        print("📥 Kết quả từ create_payment:", result)

        if result.get("success"):
            return jsonify({"message": "Tạo thanh toán thành công."}), 201
        return jsonify({"error": result.get("error")}), 400

    except Exception as e:
        print("🔥 Lỗi trong create_payment:", str(e))
        return jsonify({"error": str(e)}), 500


@payment_bp.route("/<int:payment_id>", methods=["PUT"])
def update_payment(payment_id):
    data = request.get_json()
    result = PaymentService.update_payment(payment_id, data)
    if result.get("success"):
        return jsonify({"message": "Payment updated successfully"}), 200
    return jsonify({"error": result.get("error")}), 400


@payment_bp.route("/<int:payment_id>", methods=["DELETE"])
def delete_payment(payment_id):
    result = PaymentService.delete_payment(payment_id)
    if result.get("success"):
        return jsonify({"message": "Payment deleted successfully"}), 200
    return jsonify({"error": result.get("error")}), 400


