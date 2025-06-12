import re
from flask import Blueprint, render_template, redirect, request, session, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user

from app.services.account_service import AccountService
from app.utils.email_sender import generate_and_send_otp, verify_otp
from .forms import LoginForm, RegistrationForm
from ..models import Account
from . import auth
from ..services.customer_service import CustomerService
from ..services.plan_service import PlanService
from ..services.subscriber_service import SubscriberService
from ..services.subscription_service import SubscriptionService

email_otp_verified = set()


@auth.route("/login", methods=["GET", "POST"])
def login():
    print("current_user", current_user)
    if current_user.get_id():
        return redirect(url_for("main_bp.index"))

    form = LoginForm()
    if form.validate_on_submit():
        result = AccountService.check_login(form.email.data, form.password.data)

        if result.get("success"):
            user = result["data"]["account_id"]
            print("user", user)

            user_data = result.get("data", {})
            print("user_data", user_data)
            role = user_data.get("role_type")
            login_user(user)  # cần đảm bảo `user` là instance của UserMixin
            session.permanent = True
            # ✅ Gán session theo role_type
            session["role_type"] = role

            if role == "staff":
                session["staff_id"] = user_data.get("staff_id")
                session["full_name"] = user_data.get("full_name")
                session["email"] = user_data.get("email")
                session["phone"] = user_data.get("phone")
                session["gender"] = user_data.get("gender")

            elif role == "subscriber":
                session["subscriber_id"] = user_data.get("subscriber_id")

                session["full_name"] = user_data.get(
                    "customer_name"
                )  # lấy tên từ customer
                session["phone"] = user_data.get("phone_number")
                session["main_balance"] = user_data.get("main_balance")
                session["subscriber_type"] = user_data.get("subscriber_type")
                flash(result.get("message"), "success")

            # ➤ Điều hướng theo role
            if result["data"]["role_type"] == "staff":
                print("staff")
                return redirect(url_for("admin_main_bp.index"))
            else:
                return redirect(url_for("main_bp.index"))
        else:
            flash(result.get("message"), "danger")
            return render_template("auth/login.html", form=form)

    return render_template("auth/login.html", form=form)


@auth.route("/logout")
@login_required
def logout():
    print("logout", current_user)
    logout_user()
    session.clear()
    return redirect(url_for("main_bp.index"))


@auth.route("/register", methods=["GET", "POST"])
def register():
    # if current_user:
    #     return redirect(url_for("main_bp.index"))
    form = RegistrationForm()
    data = {"username": form.username.data, "password": form.password.data}
    if form.validate_on_submit():
        result = AccountService.create_account(data)
        flash(result["message"])
        if result["success"]:

            return redirect(url_for("auth.login"))
        else:
            # flash(result["message"])
            return redirect(url_for("auth.register"))
    return render_template("auth/register.html", form=form)


@auth.route("/subscribers/<int:subscriber_id>", methods=["GET"])
def view_subscriber(subscriber_id):
    # Lấy thông tin của subscriber, customer và subscription
    subscriber = SubscriberService.get_subscriber_by_id(subscriber_id)
    customer = CustomerService.get_customer_by_id(subscriber.customer_id)
    subscriptions = SubscriptionService.get_plan_exp(subscriber_id)

    # In ra các dữ liệu trước khi truyền vào HTML
    print("Subscriber: ", subscriber)
    print("Customer: ", customer)
    print("Subscription: ", subscriptions)

    # Truyền các dữ liệu vào HTML template
    return render_template(
        "home/cuoc.html",
        subscriber=subscriber,
        customer=customer,
        subscriptions=subscriptions,
    )
@auth.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    step = int(request.args.get("step", 1))
    email_or_phone = request.args.get("email", "")

    if request.method == "POST":
        form_data = request.form.to_dict()

        if step == 1:
            # BƯỚC 1: Gửi mã xác thực
            email_or_phone = form_data.get("email_or_phone", "").strip()

            if not re.match(r"[^@]+@[^@]+\.[^@]+", email_or_phone):
                flash("⚠️ Email không hợp lệ.", "danger")
                return redirect(url_for("auth.forgot_password", step=1))

            try:
                generate_and_send_otp(email_or_phone)
                flash("📨 Mã xác nhận đã được gửi đến email của bạn.", "info")
                return redirect(
                    url_for("auth.forgot_password", step=2, email=email_or_phone)
                )
            except Exception as e:
                flash("❌ Gửi email thất bại: " + str(e), "danger")
                return redirect(url_for("auth.forgot_password", step=1))

        elif step == 2:
            # BƯỚC 2: Xác nhận OTP
            email_or_phone = form_data.get("email_or_phone", "").strip()
            otp = form_data.get("otp", "").strip()

            if verify_otp(email_or_phone, otp):
                email_otp_verified.add(email_or_phone)
                flash("✅ Xác minh thành công. Vui lòng đặt lại mật khẩu.", "success")
                return redirect(
                    url_for("auth.forgot_password", step=3, email=email_or_phone)
                )
            else:
                flash("❌ Mã OTP không đúng hoặc đã hết hạn.", "danger")
                return redirect(
                    url_for("auth.forgot_password", step=2, email=email_or_phone)
                )

        elif step == 3:
            # BƯỚC 3: Đặt lại mật khẩu
            email_or_phone = form_data.get("email_or_phone", "").strip()
            new_password = form_data.get("new_password", "")
            confirm_password = form_data.get("confirm_password", "")

            if new_password != confirm_password:
                flash("❌ Mật khẩu xác nhận không khớp.", "danger")
                return redirect(
                    url_for("auth.forgot_password", step=3, email=email_or_phone)
                )

            if email_or_phone not in email_otp_verified:
                flash("⚠️ Bạn cần xác minh OTP trước khi đặt lại mật khẩu.", "danger")
                return redirect(url_for("auth.forgot_password", step=1))

            try:
                AccountService.reset_password_by_email_or_phone(
                    email_or_phone, new_password
                )
                flash(
                    "✅ Mật khẩu đã được đặt lại thành công. Bạn có thể đăng nhập lại.",
                    "success",
                )
                return redirect(url_for("auth.login"))
            except Exception as e:
                flash(f"❌ Có lỗi khi đặt lại mật khẩu: {str(e)}", "danger")
                return redirect(
                    url_for("auth.forgot_password", step=3, email=email_or_phone)
                )

    return render_template(
        "auth/forgot_password.html", step=step, email_or_phone=email_or_phone
    )
