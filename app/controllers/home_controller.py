from flask import Blueprint, render_template

from flask import app
from flask_login import current_user, login_required, logout_user

from app.services.account_service import AccountService

main_bp = Blueprint("main_bp", __name__, url_prefix="/")


@main_bp.route("/")
@login_required
def index():
    user = None

    print("current-use", current_user)
    if current_user.is_authenticated:
        print("có")
        user = AccountService.get_account_by_id(current_user.id)
    return render_template("home/index.html", current_user=user)
