# app/controllers/otp_controller.py

from flask import Blueprint, request, jsonify
from app.utils.email_sender import generate_and_send_otp, verify_otp
from flask_login import login_required
from app.utils.decorator import required

otp_bp = Blueprint("otp", __name__, url_prefix="/otp")


@otp_bp.route("/send", methods=["POST"])
def send_otp():
    data = request.get_json()
    email = data.get("email")
    if not email:
        return (
            jsonify(
                {
                    "success": False,
                    "error": "Thiếu địa chỉ email",
                    "message": "Vui lòng cung cấp email",
                    "data": None,
                }
            ),
            400,
        )

    try:
        generate_and_send_otp(email)
        return (
            jsonify(
                {
                    "success": True,
                    "error": None,
                    "message": "Mã xác nhận đã được gửi",
                    "data": None,
                }
            ),
            200,
        )
    except Exception as e:
        return (
            jsonify(
                {
                    "success": False,
                    "error": str(e),
                    "message": "Không thể gửi email",
                    "data": None,
                }
            ),
            500,
        )


@otp_bp.route("/verify", methods=["POST"])
def verify_otp_code():
    data = request.get_json()
    email = data.get("email")
    otp = data.get("otp")

    if verify_otp(email, otp):
        return (
            jsonify(
                {
                    "success": True,
                    "error": None,
                    "message": "Mã xác nhận hợp lệ",
                    "data": None,
                }
            ),
            200,
        )
    return (
        jsonify(
            {
                "success": False,
                "error": "OTP không đúng hoặc đã hết hạn",
                "message": "Xác minh thất bại",
                "data": None,
            }
        ),
        400,
    )
