from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user

from app.services.account_service import AccountService
from .forms import LoginForm, RegistrationForm
from ..models import Account
from . import auth

# auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    # logout_user()
    print("cus", current_user)
    # if current_user:
    #     return redirect(url_for("main_bp.index"))

    form = LoginForm()
    if form.validate_on_submit():
        result = AccountService.check_login(form.email.data, form.password.data)
        print("🧾 Kết quả đăng nhập:", result.get("data"))

        if result.get("success"):
            user = result["data"]
            print("use", user.to_dict(), current_user)
            login_user(user)
            flash(result.get("message"), "success")
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
    if form.validate_on_submit():
        AccountService.create_account(form.username.data, form.password.data)
        flash("Congratulations, you are now a registered user!")
        return redirect(url_for("auth.login"))
    return render_template("auth/register.html", form=form)
