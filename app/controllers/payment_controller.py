from flask import Blueprint, request, jsonify
from app.services.payment_service import PaymentService

payment_bp = Blueprint("payment", __name__, url_prefix="/payments")


@payment_bp.route("/", methods=["GET"])
def get_all_payments():
    payments = PaymentService.get_all_payments()
    return jsonify(payments), 200


@payment_bp.route("/<int:payment_id>", methods=["GET"])
def get_payment_by_id(payment_id):
    payment = PaymentService.get_payment_by_id(payment_id)
    if payment:
        return jsonify(payment.to_dict()), 200
    return jsonify({"error": "Payment not found"}), 404


@payment_bp.route("/", methods=["POST"])
def create_payment():
    data = request.get_json()
    result = PaymentService.create_payment(data)
    if result.get("success"):
        return jsonify({"message": "Payment created successfully"}), 201
    return jsonify({"error": result.get("error")}), 400


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
