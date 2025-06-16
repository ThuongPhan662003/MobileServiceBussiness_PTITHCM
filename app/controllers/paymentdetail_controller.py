from flask import Blueprint, request, jsonify
from app.services.paymentdetail_service import PaymentDetailService
from flask_login import login_required
from app.utils.decorator import required

payment_detail_bp = Blueprint("payment_detail", __name__, url_prefix="/payment-details")


@login_required
@payment_detail_bp.route("/", methods=["GET"])
@required
def get_all_payment_details():
    payment_details = PaymentDetailService.get_all_payment_details()
    return jsonify(payment_details), 200


@login_required
@payment_detail_bp.route("/<int:payment_detail_id>", methods=["GET"])
@required
def get_payment_detail_by_id(payment_detail_id):
    payment_detail = PaymentDetailService.get_payment_detail_by_id(payment_detail_id)
    if payment_detail:
        return jsonify(payment_detail.to_dict()), 200
    return jsonify({"error": "Payment detail not found"}), 404


@login_required
@payment_detail_bp.route("/<int:payment_id>/<int:plan_id>", methods=["POST"])
@required
def create_payment_detail(payment_id: int, plan_id: int):
    result = PaymentDetailService.create_payment_detail(payment_id, plan_id)

    status_code = 200 if result.get("success") else 400

    return (
        jsonify(
            {
                "success": result.get("success", False),
                "error": result.get("error"),
                "message": result.get("message"),
                "data": result.get("data"),
            }
        ),
        status_code,
    )


@login_required
@payment_detail_bp.route("/<int:payment_detail_id>", methods=["PUT"])
@required
def update_payment_detail(payment_detail_id):
    data = request.get_json()
    result = PaymentDetailService.update_payment_detail(payment_detail_id, data)
    if result.get("success"):
        return jsonify({"message": "Payment detail updated successfully"}), 200
    return jsonify({"error": result.get("error")}), 400


@login_required
@payment_detail_bp.route("/<int:payment_detail_id>", methods=["DELETE"])
@required
def delete_payment_detail(payment_detail_id):
    result = PaymentDetailService.delete_payment_detail(payment_detail_id)
    if result.get("success"):
        return jsonify({"message": "Payment detail deleted successfully"}), 200
    return jsonify({"error": result.get("error")}), 400


