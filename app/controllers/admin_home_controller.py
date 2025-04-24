from flask import Blueprint, render_template, session
from flask_login import current_user


admin_main_bp = Blueprint("admin_main_bp", __name__, url_prefix="/admin")


@admin_main_bp.route("/")
def index():
    print("Hello")
    print("curgetddđ", current_user.get_id())
    # send_email(
    #     subject="Welcome to Our Service!",
    #     recipient="n21dccn184@student.ptithcm.edu.vn",
    #     template="welcome",
    #     name="thuong",  # Truyền các tham số vào template
    # )

    return render_template("admin_home/index.html")
