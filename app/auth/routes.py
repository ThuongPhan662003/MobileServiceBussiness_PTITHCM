from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user

from app.services.account_service import AccountService
from .forms import LoginForm, RegistrationForm
from ..models import Account
from . import auth

# auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():

    if current_user.is_authenticated:
        return redirect(url_for("main_bp.index"))

    form = LoginForm()
    if form.validate_on_submit():
        user = AccountService.check_login(form.email.data, form.password.data)
        print("login_success", user)
        if user:
            login_user(user)
            return redirect(url_for("main_bp.index"))
        flash("Tên đăng nhập hoặc mật khẩu không đúng.", "danger")
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
