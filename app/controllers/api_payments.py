from datetime import datetime, timezone

import hashlib
from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    jsonify,
    url_for,
)
import paypalrestsdk
import urllib
import hmac
import urllib.parse
from app.forms.payments.payment_form import PaymentForm
from app.services.payment_service import PaymentService
from app.utils import vnpay
from app.utils.ip import get_client_ip


payment_api_bp = Blueprint("payment", __name__, url_prefix="/pay-process")


@payment_api_bp.route("/", methods=["GET"])
def index():
    print(".")
    return render_template("payments/user/index.html")


@payment_api_bp.route("/vnpay_pay", methods=["POST", "GET"])
def vnpay_pay():
    form = PaymentForm(request.form)
    if request.method == "POST" and form.validate():
        order_type = form.order_type.data
        order_id = form.order_id.data
        amount = form.amount.data
        order_desc = form.order_desc.data
        bank_code = form.bank_code.data
        language = form.language.data
        ipaddr = get_client_ip(request)

        vnp = vnpay()
        print(vnp)
        vnp.requestData.update(
            {
                "vnp_Version": "2.1.0",
                "vnp_Command": "pay",
                "vnp_TmnCode": current_app.config["VNPAY_TMN_CODE"],
                "vnp_Amount": int(amount * 100),
                "vnp_CurrCode": "VND",
                "vnp_TxnRef": order_id,
                "vnp_OrderInfo": order_desc,
                "vnp_OrderType": order_type,
                "vnp_Locale": language or "vn",
                "vnp_CreateDate": datetime.now().strftime("%Y%m%d%H%M%S"),
                "vnp_IpAddr": ipaddr,
                "vnp_ReturnUrl": current_app.config["VNPAY_RETURN_URL"],
            }
        )
        print("vnp", vnp)
        if bank_code:
            vnp.requestData["vnp_BankCode"] = bank_code
        print("a")
        payment_url = vnp.get_payment_url()
        print("return", payment_url)
        return redirect(payment_url)

    return render_template("payments/user/payment.html", form=form, title="Thanh toán")


@payment_api_bp.route("/vnpay_return")
def vnpay_return():
    # Lấy tất cả tham số VNPAY trả về
    vnp = vnpay()
    vnp.responseData = request.args.to_dict()

    # Kiểm tra checksum
    is_valid = vnp.validate_signature(current_app.config["VNPAY_HASH_SECRET_KEY"])
    if not is_valid:
        flash("Chữ ký không hợp lệ. Giao dịch bị từ chối.", "danger")
        return render_template(
            "payment_result.html", success=False, data=vnp.responseData
        )

    # Đọc kết quả
    rsp_code = vnp.responseData.get("vnp_ResponseCode")  # '00' = thành công
    txn_ref = vnp.responseData.get("vnp_TxnRef")
    amount = int(vnp.responseData.get("vnp_Amount", 0)) / 100  # chia lại
    pay_date = vnp.responseData.get("vnp_PayDate")

    if rsp_code == "00":
        # TODO: cập nhật trạng thái đơn hàng trong DB của bạn

        flash(
            f"Thanh toán thành công! Mã đơn: {txn_ref}, Số tiền: {amount} VND",
            "success",
        )
        success = True
    else:

        flash(f"Thanh toán thất bại (code: {rsp_code}). Vui lòng thử lại.", "warning")
        success = False

    return render_template(
        "payments/user/payment_result.html",
        success=success,
        data={
            "order_id": txn_ref,
            "amount": amount,
            "response_code": rsp_code,
            "pay_date": pay_date,
            **vnp.responseData,
        },
    )


@payment_api_bp.route("/pay")
def pay_paypal():
    payment = paypalrestsdk.Payment(
        {
            "intent": "sale",
            "payer": {"payment_method": "paypal"},
            "redirect_urls": {
                "return_url": url_for("payment_bp.payment_execute", _external=True),
                "cancel_url": url_for("payment_bp.payment_cancel", _external=True),
            },
            "transactions": [
                {
                    "item_list": {
                        "items": [
                            {
                                "name": "Test Item",
                                "sku": "12345",
                                "price": "10.00",
                                "currency": "USD",
                                "quantity": 1,
                            }
                        ]
                    },
                    "amount": {"total": "10.00", "currency": "USD"},
                    "description": "Thanh toán thử nghiệm với PayPal",
                }
            ],
        }
    )

    if payment.create():
        # Tìm link redirect tới PayPal để người dùng thanh toán
        for link in payment.links:
            if link.method == "REDIRECT":
                return redirect(link.href)
    else:
        flash("Tạo payment thất bại: " + payment.error["message"])
        return redirect(url_for("payment_bp.index"))


@payment_api_bp.route("/execute")
def payment__paypal_execute():
    payment_id = request.args.get("paymentId")
    payer_id = request.args.get("PayerID")
    payment = paypalrestsdk.Payment.find(payment_id)

    if payment.execute({"payer_id": payer_id}):
        # Thanh toán thành công
        return render_template(
            "payments/user/payment_result.html",
            status="success",
            provider="PayPal",
            details={
                "Payment ID": payment.id,
                "Status": payment.state,
                "Amount": f"{payment.transactions[0].amount.total} {payment.transactions[0].amount.currency}",
            },
        )
    else:
        # Thanh toán thất bại
        return render_template(
            "payments/user/payment_result.html",
            status="failure",
            provider="PayPal",
            message=payment.error.get("message", "Unknown error"),
        )


@payment_api_bp.route("/cancel")
def payment__paypal_cancel():
    # Người dùng hủy thanh toán
    return render_template(
        "payments/user/payment_result.html", status="cancel", provider="PayPal"
    )
