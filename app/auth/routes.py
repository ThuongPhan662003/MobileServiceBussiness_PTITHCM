from flask import Blueprint, render_template, redirect, session, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user

from app.services.account_service import AccountService
from .forms import LoginForm, RegistrationForm
from ..models import Account
from . import auth

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
