from datetime import datetime, timezone

from decimal import Decimal
import hashlib
from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    jsonify,
    session,
    url_for,
)
from flask_login import current_user, login_required
import paypalrestsdk
import urllib
import hmac
import urllib.parse
from app.forms.payments.payment_form import PaymentForm
from app.models.subscription import Subscription
from app.services.payment_service import PaymentService
from app.services.plan_service import PlanService
from app.services.subscriber_service import SubscriberService
from app.services.subscription_service import SubscriptionService
from app.utils.vnpay import VnPay
from app.utils.ip import get_client_ip


payment_api_bp = Blueprint("payment_api_bp", __name__, url_prefix="/pay-process")


@payment_api_bp.route("/", methods=["GET"])
@login_required
def index():
    print("vô")
    code = request.args.get("plan_code")
    price = request.args.get("price")
    plan_id = request.args.get("plan_id", type=int)
    print("dữ liệu", code, price, plan_id)
    if not code or not price or not plan_id:
        flash("Thiếu thông tin gói cước cần thanh toán", "danger")
        return redirect(url_for("main_bp.index"))

    return render_template(
        "payments/user/index.html",
        item_name=code,
        vnd_price=price,
        usd_price=float(price) / 25000,
        plan_id=plan_id,
    )


@payment_api_bp.route("/vnpay_pay", methods=["POST", "GET"])
@login_required
def vnpay_pay():
    form = PaymentForm(request.form)
    if request.method == "POST" and form.validate():
        order_type = form.order_type.data
        order_id = form.order_id.data
        amount = form.amount.data
        order_desc = form.order_desc.data
        bank_code = form.bank_code.data
        language = form.language.data or "vn"
        ipaddr = get_client_ip(request)

        # ✅ Import đúng class
        from app.utils.vnpay import VnPay

        vnp = VnPay()

        # ✅ Chuẩn bị dữ liệu để ký
        vnp.requestData = {
            "vnp_Version": "2.1.0",
            "vnp_Command": "pay",
            "vnp_TmnCode": current_app.config["VNPAY_TMN_CODE"],
            "vnp_Amount": int(amount) * 100,  # Đơn vị là *100
            "vnp_CurrCode": "VND",
            "vnp_TxnRef": order_id,
            "vnp_OrderInfo": order_desc,
            "vnp_OrderType": order_type,
            "vnp_Locale": language,
            "vnp_ReturnUrl": current_app.config["VNPAY_RETURN_URL"],
            "vnp_IpAddr": ipaddr,
            "vnp_CreateDate": datetime.now().strftime("%Y%m%d%H%M%S"),
        }

        # ✅ Thêm bank nếu có
        if bank_code:
            vnp.requestData["vnp_BankCode"] = bank_code

        # ✅ Tạo URL thanh toán
        payment_url = vnp.get_payment_url(
            current_app.config["VNPAY_URL"], current_app.config["VNPAY_HASH_SECRET"]
        )

        # ✅ In để kiểm tra debug
        print("VNPAY redirect URL:", payment_url)

        return redirect(payment_url)

    return render_template("payments/user/payment.html", form=form, title="Thanh toán")


@payment_api_bp.route("/vnpay_return")
@login_required
def vnpay_return():
    # Lấy tất cả tham số VNPAY trả về
    vnp = VnPay()
    vnp.responseData = request.args.to_dict()

    # Kiểm tra checksum
    is_valid = vnp.validate_signature(current_app.config["VNPAY_HASH_SECRET"])
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
@login_required
def pay_paypal():
    # Lấy giá VND từ giao diện
    # vnd_price = float(request.form.get("item_price_vnd"))  # ví dụ 250000 VND
    # usd_price = round(vnd_price / 25000, 2)  # Tạm quy đổi: 1 USD = 25,000 VND

    # item_name = request.form.get("item_name")
    # package_id = request.form.get("package_id")
    vnd_price = 25000  # ví dụ 250000 VND
    usd_price = round(vnd_price / 25000, 2)  # Tạm quy đổi: 1 USD = 25,000 VND

    item_name = "5G30"
    package_id = "1"

    session["vnd_price"] = vnd_price
    session["usd_price"] = usd_price
    session["item_name"] = item_name
    session["package_id"] = package_id

    payment = paypalrestsdk.Payment(
        {
            "intent": "sale",
            "payer": {"payment_method": "paypal"},
            "redirect_urls": {
                "return_url": url_for(
                    "payment_api_bp.payment_paypal_execute", _external=True
                ),
                "cancel_url": url_for(
                    "payment_api_bp.payment_paypal_cancel", _external=True
                ),
            },
            "transactions": [
                {
                    "item_list": {
                        "items": [
                            {
                                "name": item_name,
                                "sku": "PKG" + str(package_id),
                                "price": str(usd_price),
                                "currency": "USD",
                                "quantity": 1,
                            }
                        ]
                    },
                    "amount": {"total": str(usd_price), "currency": "USD"},
                    "description": f"Thanh toán gói cước {item_name} (≈ {vnd_price:,.0f} VND)",
                }
            ],
        }
    )

    if payment.create():
        for link in payment.links:
            if link.method == "REDIRECT":
                return redirect(link.href)
    else:
        flash("Tạo payment thất bại: " + payment.error["message"])
        return redirect(url_for("payment_api_bp.index"))


@payment_api_bp.route("/execute")
@login_required
def payment_paypal_execute():
    payment_id = request.args.get("paymentId")
    payer_id = request.args.get("PayerID")

    if not payment_id or not payer_id:
        session["payment_result"] = {
            "status": "failure",
            "provider": "PayPal",
            "message": "Thiếu thông tin xác thực thanh toán",
        }
        return redirect(url_for("payment_api_bp.payment_result"))

    payment = paypalrestsdk.Payment.find(payment_id)

    if payment.execute({"payer_id": payer_id}):
        # Lấy thông tin đơn hàng
        items = payment.transactions[0].item_list.items
        item_details = [
            {
                "name": item["name"],
                "sku": item["sku"],
                "price": item["price"],
                "currency": item["currency"],
                "quantity": item["quantity"],
            }
            for item in items
        ]

        plan_code = item_details[0].get("name")
        subscriber_data = SubscriberService.get_by_account_id(current_user.get_id())
        print("Kết quả subscriber:", subscriber_data)

        if subscriber_data:
            subscriber_id = subscriber_data["subscriber_id"]
        else:
            subscriber_id = None

        # Gọi thanh toán nếu đủ thông tin
        if plan_code and subscriber_id:
            result = PaymentService.create_transaction(
                plan_code, subscriber_id, "QRCode"
            )
            print("Kết quả thanh toán:", result)

            session["payment_result"] = {
                "status": "success" if result["success"] else "failure",
                "provider": "PayPal",
                "details": {
                    "Payment ID": payment.id,
                    "Status": payment.state,
                    "Amount": f"{payment.transactions[0].amount.total} {payment.transactions[0].amount.currency}",
                },
                "items": item_details,
                "message": result.get("message"),
            }

            return redirect(url_for("payment_api_bp.payment_result"))

        else:
            session["payment_result"] = {
                "status": "failure",
                "provider": "PayPal",
                "message": "Thiếu mã gói hoặc thuê bao",
            }
            return redirect(url_for("payment_api_bp.payment_result"))

    # Nếu thất bại
    session["payment_result"] = {
        "status": "failure",
        "provider": "PayPal",
        "message": payment.error.get("message", "Unknown error"),
    }
    return redirect(url_for("payment_api_bp.payment_result"))


@payment_api_bp.route("/result")
@login_required
def payment_result():
    result = session.get("payment_result")
    if not result:
        flash("Không có dữ liệu thanh toán để hiển thị.", "danger")
        return redirect(url_for("payment_api_bp.index"))

    return render_template(
        "payments/user/payment_result.html",
        status=result.get("status"),
        provider=result.get("provider"),
        details=result.get("details"),
        items=result.get("items"),
        message=result.get("message"),
    )


@payment_api_bp.route("/cancel")
@login_required
def payment_paypal_cancel():
    # Người dùng hủy thanh toán
    return render_template(
        "payments/user/payment_result.html", status="cancel", provider="PayPal"
    )
