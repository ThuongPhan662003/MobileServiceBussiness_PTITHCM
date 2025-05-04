from flask import Blueprint, request, jsonify
from flask_login import login_required
from app.services.paymentdetail_service import PaymentDetailService

payment_detail_bp = Blueprint("payment_detail", __name__, url_prefix="/payment-details")


@payment_detail_bp.route("/", methods=["GET"])
@login_required
def get_all_payment_details():
    payment_details = PaymentDetailService.get_all_payment_details()
    return jsonify(payment_details), 200


@payment_detail_bp.route("/<int:payment_detail_id>", methods=["GET"])
@login_required
def get_payment_detail_by_id(payment_detail_id):
    payment_detail = PaymentDetailService.get_payment_detail_by_id(payment_detail_id)
    if payment_detail:
        return jsonify(payment_detail.to_dict()), 200
    return jsonify({"error": "Payment detail not found"}), 404


@payment_detail_bp.route("/<int:payment_id>/<int:plan_id>", methods=["POST"])
@login_required
def create_payment_detail(payment_id: int, plan_id: int):
    result = PaymentDetailService.create_payment_detail(payment_id, plan_id)
    if result.get("success"):
        return jsonify({"message": "Payment detail created successfully"}), 201
    return jsonify({"error": result.get("error")}), 400


@payment_detail_bp.route("/<int:payment_detail_id>", methods=["PUT"])
@login_required
def update_payment_detail(payment_detail_id):
    data = request.get_json()
    result = PaymentDetailService.update_payment_detail(payment_detail_id, data)
    if result.get("success"):
        return jsonify({"message": "Payment detail updated successfully"}), 200
    return jsonify({"error": result.get("error")}), 400


@payment_detail_bp.route("/<int:payment_detail_id>", methods=["DELETE"])
@login_required
def delete_payment_detail(payment_detail_id):
    result = PaymentDetailService.delete_payment_detail(payment_detail_id)
    if result.get("success"):
        return jsonify({"message": "Payment detail deleted successfully"}), 200
    return jsonify({"error": result.get("error")}), 400
