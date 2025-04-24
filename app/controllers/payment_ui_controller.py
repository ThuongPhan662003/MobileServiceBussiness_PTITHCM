from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from app.services.payment_service import PaymentService
from app.services.paymentdetail_service import PaymentDetailService
import paypalrestsdk
import logging

payment_ui_bp = Blueprint("payment_ui_bp", __name__, url_prefix="/ui/payments")
logger = logging.getLogger(__name__)

# Configure PayPal SDK
paypalrestsdk.configure({
    "mode": "sandbox",  # Change to "live" in production
    "client_id": "YOUR_PAYPAL_CLIENT_ID",
    "client_secret": "YOUR_PAYPAL_CLIENT_SECRET"
})

@payment_ui_bp.route("/history", methods=["GET"])
def payment_history():
    payment_method = request.args.get('payment_method', 'Tất cả')
    payments = PaymentService.get_all_payments()
    return render_template("AdminPayment/payment_history.html", payments=payments, payment_method=payment_method)

@payment_ui_bp.route("/history/search", methods=["POST"])
def search_payments():
    data = request.form
    subscription_id = data.get("subscription_id")
    payment_date = data.get("payment_date")
    payment_method = data.get("payment_method")
    is_paid = data.get("is_paid")
    
    # Convert is_paid to boolean
    is_paid = 1 if is_paid == "1" else 0 if is_paid == "0" else None
    
    payments = PaymentService.search_payments(
        subscription_id=subscription_id if subscription_id else None,
        payment_date=payment_date if payment_date else None,
        payment_method=payment_method if payment_method else None,
        is_paid=is_paid
    )
    return render_template("AdminPayment/payment_history.html", payments=payments)

@payment_ui_bp.route("/history/reset", methods=["GET"])
def reset_search():
    return redirect(url_for("payment_ui_bp.payment_history"))

@payment_ui_bp.route("/details/<int:payment_id>", methods=["GET"])
def payment_details(payment_id):
    payment = PaymentService.get_payment_by_id(payment_id)
    details = PaymentDetailService.get_by_payment_id(payment_id)
    print(f"Payment details: {details}")
    if payment:
        return render_template("AdminPayment/payment_detail.html", payment=payment.to_dict(), details=details)
    return jsonify({"error": "Payment not found"}), 404

@payment_ui_bp.route("/pay/<int:payment_id>", methods=["POST"])
def initiate_payment(payment_id):
    payment = PaymentService.get_payment_by_id(payment_id)
    if not payment or payment.is_paid:
        return jsonify({"error": "Invalid or already paid payment"}), 400
    
    try:
        paypal_payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {"payment_method": "paypal"},
            "transactions": [{
                "amount": {
                    "total": str(payment.total_amount),
                    "currency": "USD"
                },
                "description": f"Payment for subscription {payment.subscription_id}"
            }],
            "redirect_urls": {
                "return_url": url_for("payment_ui_bp.payment_success", payment_id=payment_id, _external=True),
                "cancel_url": url_for("payment_ui_bp.payment_cancel", _external=True)
            }
        })
        if paypal_payment.create():
            # Update payment status to paid (simplified for demo)
            PaymentService.update_payment(payment_id, {
                "subscription_id": payment.subscription_id,
                "payment_date": payment.payment_date,
                "total_amount": payment.total_amount,
                "payment_method": payment.payment_method,
                "is_paid": True,
                "due_date": payment.due_date
            })
            return jsonify({"approval_url": paypal_payment.links[1].href}), 201
        else:
            logger.error(f"PayPal payment creation failed: {paypal_payment.error}")
            return jsonify({"error": "Failed to initiate PayPal payment"}), 400
    except Exception as e:
        logger.error(f"Error initiating payment: {e}")
        return jsonify({"error": "Internal server error"}), 500

@payment_ui_bp.route("/payment/success/<int:payment_id>", methods=["GET"])
def payment_success(payment_id):
    return redirect(url_for("payment_ui_bp.payment_history"))

@payment_ui_bp.route("/payment/cancel", methods=["GET"])
def payment_cancel():
    return redirect(url_for("payment_ui_bp.payment_history"))