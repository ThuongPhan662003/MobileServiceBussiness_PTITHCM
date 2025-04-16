from flask import Blueprint, render_template

from flask import app
from flask_login import current_user, logout_user

from app.services.account_service import AccountService

main_bp = Blueprint("main_bp", __name__, url_prefix="/")


@main_bp.route("/")
def index():
    user = None
    if current_user.is_authenticated:
        user = AccountService.get_account_by_id(current_user.id)
    return render_template("home/index.html", current_user=user)
