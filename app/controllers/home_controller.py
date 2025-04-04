from flask import Blueprint, render_template

from flask import app
main_bp = Blueprint("main_bp", __name__, url_prefix="/")


@main_bp.route("/")
def index():
    print("main")
    return render_template("home/index.html")
