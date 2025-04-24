from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user

from app.services.account_service import AccountService
from .forms import LoginForm, RegistrationForm
from ..models import Account
from . import auth
from ..services.customer_service import CustomerService
from ..services.plan_service import PlanService
from ..services.subscriber_service import SubscriberService
from ..services.subscription_service import SubscriptionService


# auth = Blueprint("auth", __name__)


# @auth.route("/login", methods=["GET", "POST"])
# def login():
#     print("current_usre", current_user)
#     if current_user.get_id():
#         return redirect(url_for("main_bp.index"))

#     form = LoginForm()
#     if form.validate_on_submit():
#         result = AccountService.check_login(form.email.data, form.password.data)
#         print("🧾 Kết quả đăng nhập:", result.get("data"))

#         if result.get("success"):
#             user = result["data"]
#             print("user", user)
#             login_user(user)
#             flash(result.get("message"), "success")
#             return redirect(url_for("main_bp.index"))
#         else:
#             flash(result.get("message"), "danger")


#     return render_template("auth/login.html", form=form)
@auth.route("/login", methods=["GET", "POST"])
def login():
    print("current_user", current_user)
    if current_user.get_id():
        return redirect(url_for("main_bp.index"))

    form = LoginForm()
    if form.validate_on_submit():
        result = AccountService.check_login(form.email.data, form.password.data)
        print("🧾 Kết quả đăng nhập:", result["data"])

        if result.get("success"):
            user = result["data"]["account_id"]
            print("user", user)

            login_user(user)  # cần đảm bảo `user` là instance của UserMixin

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


@auth.route("/logout")
@login_required
def logout():
    print("logout", current_user)
    logout_user()
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
@auth.route("/customers/<int:subscriber_id>", methods=["GET"])
def view_customer(subscriber_id):
    subscriber = SubscriberService.get_subscriber_by_id(subscriber_id)
    if subscriber:
        customer = CustomerService.get_customer_by_id(subscriber.customer_id)
        return render_template("home/tb.html", subscriber=subscriber, customer=customer)
    return "Thuê bao không tồn tại", 404
@auth.route("/subscribers/<int:subscriber_id>", methods=["GET"])
def view_subscriber(subscriber_id):
    subscriber = SubscriberService.get_subscriber_by_id(subscriber_id)
    if subscriber:
        customer = CustomerService.get_customer_by_id(subscriber.customer_id)
        return render_template("home/cuoc.html", subscriber=subscriber, customer=customer)
    return "Thuê bao không tồn tại", 404