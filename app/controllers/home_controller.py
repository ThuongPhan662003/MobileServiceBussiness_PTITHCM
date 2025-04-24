from flask import Blueprint, render_template, session

from flask import app
from flask_login import current_user, login_required, logout_user

from app.services.account_service import AccountService

main_bp = Blueprint("main_bp", __name__, url_prefix="/")


@main_bp.route("/")
def index():

    user = None
    # print("curgetddđ", current_user.get_id(), session["subscriber_id"])
    if current_user.get_id():
        print("cos")
        user = AccountService.get_account_by_id(current_user.get_id())
    return render_template("home/index.html", current_user=user)
