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
    print("login start")
    flash("Email hoặc mật khẩu không đúng.", "danger")
    form = LoginForm()

    if form.validate_on_submit():
        print("login")
        user = Account.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(1, remember=form.remember.data)
        return redirect(url_for("main_bp.index"))
        # flash("Invalid email or password")
    return render_template("auth/login.html", form=form)


@auth.route("/logout")
@login_required
def logout():
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
