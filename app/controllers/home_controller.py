from flask import Blueprint, render_template, session

from flask import app
from flask_login import current_user, login_required, logout_user

from app.services.account_service import AccountService

main_bp = Blueprint("main_bp", __name__, url_prefix="/")


@main_bp.route("/")
def index():

    user = None
    return render_template("home/index.html")
