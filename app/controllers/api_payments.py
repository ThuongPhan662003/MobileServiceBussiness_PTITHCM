from datetime import datetime, timezone
from flask_login import login_required
from app.utils.decorator import required
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


@login_required
@payment_api_bp.route("/", methods=["GET"])
@required
def index_payment_api():
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


@login_required
@payment_api_bp.route("/deposit-index", methods=["POST"])
# @required
def deposit():
    money = float(request.form.get("amount", 0))
    return render_template("payments/user/deposit.html", money=money)


@login_required
@payment_api_bp.route("/deposit-pay", methods=["POST"])
def deposit_pay():
    try:
        vnd_price = request.form.get("money", type=float)
        if not vnd_price or vnd_price <= 0:
            flash("Số tiền nạp không hợp lệ.", "danger")
            return redirect(url_for("payment_api_bp.deposit"))

        usd_price = round(vnd_price / 25000, 2)

        # Lưu session để dùng lại
        session["vnd_price"] = vnd_price
        session["usd_price"] = usd_price
        session["item_name"] = f"Nạp {vnd_price:,.0f} VND"

        payment = paypalrestsdk.Payment(
            {
                "intent": "sale",
                "payer": {"payment_method": "paypal"},
                "redirect_urls": {
                    "return_url": url_for(
                        "payment_api_bp.deposit_execute", _external=True
                    ),
                    "cancel_url": url_for(
                        "payment_api_bp.deposit_paypal_cancel", _external=True
                    ),
                },
                "transactions": [
                    {
                        "item_list": {
                            "items": [
                                {
                                    "name": "Nạp tiền",
                                    "sku": "DEPOSIT",
                                    "price": str(usd_price),
                                    "currency": "USD",
                                    "quantity": 1,
                                }
                            ]
                        },
                        "amount": {"total": str(usd_price), "currency": "USD"},
                        "description": f"Nạp tiền vào ví (≈ {vnd_price:,.0f} VND)",
                    }
                ],
            }
        )

        if payment.create():
            # Lưu Payment ID để xử lý execute sau này
            session["payment_id"] = payment.id
            for link in payment.links:
                if link.method == "REDIRECT":
                    return redirect(link.href)

        flash("Tạo yêu cầu thanh toán thất bại: " + payment.error["message"], "danger")
        return redirect(url_for("payment_api_bp.deposit_result"))

    except Exception as e:
        flash(f"Lỗi: {str(e)}", "danger")
        return redirect(url_for("payment_api_bp.deposit"))


@login_required
@payment_api_bp.route("/deposit-execute", methods=["GET"])
def deposit_execute():
    payment_id = session.get("payment_id")
    payer_id = request.args.get("PayerID")

    if not payment_id or not payer_id:
        session["payment_result"] = {
            "status": "failure",
            "provider": "PayPal",
            "message": "Thiếu thông tin xác thực thanh toán.",
        }
        return redirect(url_for("payment_api_bp.deposit_result"))

    payment = paypalrestsdk.Payment.find(payment_id)

    if payment.execute({"payer_id": payer_id}):
        amount = payment.transactions[0].amount.total
        currency = payment.transactions[0].amount.currency
        print("amountđ", amount, currency)
        subscriber = SubscriberService.get_subscriber_by_id(session["subscriber_id"])
        data = {
            "phone_number": subscriber.phone_number,
            "main_balance": subscriber.main_balance
            + (Decimal(str(amount)) * Decimal("25000")),
            "customer_id": subscriber.customer_id,
            "account_id": subscriber.account_id,
            "expiration_date": None,
            "warning_date": None,
            "is_active": str(subscriber.is_active).lower(),
            "subscriber": subscriber.subscriber_type,
        }
        result = SubscriberService.update_subscriber(session["subscriber_id"], data)
        if result.get("success"):

            session["payment_result"] = {
                "status": "success",
                "provider": "PayPal",
                "details": {
                    "Payment ID": payment.id,
                    "Status": payment.state,
                    "Amount": f"{amount} {currency}",
                },
                "items": [
                    {
                        "name": item.name,
                        "price": item.price,
                        "currency": item.currency,
                        "quantity": item.quantity,
                    }
                    for item in payment.transactions[0].item_list.items
                ],
                "message": "Thanh toán thành công!",
            }

            return redirect(url_for("payment_api_bp.deposit_result"))

    session["payment_result"] = {
        "status": "failure",
        "provider": "PayPal",
        "message": payment.error.get("message", "Đã có lỗi xảy ra."),
    }
    return redirect(url_for("payment_api_bp.deposit_result"))


@login_required
@payment_api_bp.route("/deposit-result")
def deposit_result():
    result = session.get("payment_result")
    if not result:
        flash("Không có dữ liệu thanh toán để hiển thị.", "danger")
        return redirect(url_for("payment_api_bp.deposit"))

    return render_template(
        "payments/user/deposit_result.html",
        status=result.get("status"),
        provider=result.get("provider"),
        details=result.get("details"),
        items=result.get("items"),
        message=result.get("message"),
    )


# 3. HỦY GIAO DỊCH
@login_required
@payment_api_bp.route("/cancel")
def deposit_paypal_cancel():
    session["payment_result"] = {
        "status": "failure",
        "provider": "PayPal",
        "message": "Giao dịch đã bị huỷ bởi người dùng.",
    }
    return redirect(url_for("payment_api_bp.deposit_result"))


@login_required
@payment_api_bp.route("/vnpay_return")
@required
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


@login_required
@payment_api_bp.route("/pay")
@required
def pay_paypal():
    # Lấy giá VND từ giao diện
    # print("Vào hàm pay_paypal", request.form.get("item_price_vnd"))
    # vnd_price = float(request.form.get("item_price_vnd"))  # ví dụ 250000 VND
    # # usd_price = round(vnd_price / 25000, 2)  # Tạm quy đổi: 1 USD = 25,000 VND

    # item_name = request.form.get("item_name")
    # package_id = request.form.get("package_id")
    item_name = request.args.get("item_name")
    vnd_price = request.args.get("item_price_vnd", type=float)
    package_id = request.args.get("package_id", type=int)

    print("✔️ item_name:", item_name)
    print("✔️ vnd_price:", vnd_price)
    print("✔️ plan_id:", package_id)
    print("item_name", item_name)
    # vnd_price = 25000  # ví dụ 250000 VND
    usd_price = round(vnd_price / 25000, 2)  # Tạm quy đổi: 1 USD = 25,000 VND

    # item_name = "5G30"
    # package_id = "1"

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


@login_required
@payment_api_bp.route("/execute")
@required
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


@login_required
@payment_api_bp.route("/result")
@required
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


@login_required
@payment_api_bp.route("/cancel")
@required
def payment_paypal_cancel():
    # Người dùng hủy thanh toán
    return render_template(
        "payments/user/payment_result.html", status="cancel", provider="PayPal"
    )
