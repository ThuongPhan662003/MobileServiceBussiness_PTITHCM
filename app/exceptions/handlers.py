from flask import flash, redirect, render_template, session, url_for
from flask_login import current_user, logout_user
from app.exceptions import exceptions
from app.exceptions.custom_exception import CustomException


# @exceptions.app_errorhandler(404)
# def not_found_error(error):
#     print("404 error")
#     return render_template("404.html"), 404


# @exceptions.app_errorhandler(500)
# def internal_error(error):
#     print("500 error")
#     return render_template("500.html"), 500


@exceptions.before_request
def check_session_expired():
    if current_user.get_id() and not session.get("_permanent"):
        logout_user()
        session.clear()
        flash("Phiên đăng nhập của bạn đã hết hạn. Vui lòng đăng nhập lại.", "warning")
        return redirect(url_for("auth.login"))
