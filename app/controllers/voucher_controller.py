from flask import Blueprint, render_template, request, jsonify

from flask_login import current_user
from app.services.staff_service import StaffService

from app.services.voucher_service import VoucherService
from flask_login import login_required
from app.utils.decorator import required

voucher_bp = Blueprint("voucher", __name__, url_prefix="/vouchers")


@login_required
@voucher_bp.route("/", methods=["GET"])
@required
def voucher_list():
    all_vouchers = VoucherService.get_all_vouchers()
    print("all_vouchers", all_vouchers)
    return render_template("vouchers/voucher_list.html", vouchers=all_vouchers)


@login_required
@voucher_bp.route("/", methods=["POST"])
@required
def voucher_create():
    data = request.get_json()
    print("Received data:", StaffService.get_staff_by_account_id(current_user.get_id()))
    data["staff_id"] = StaffService.get_staff_by_account_id(current_user.get_id())
    result = VoucherService.create_voucher(data)
    print("Service result:", result)

    if result.get("success"):

        return (
            jsonify(
                {
                    "success": True,
                    "error": False,
                    "message": result.get("message", "Voucher created successfully."),
                }
            ),
            200,
        )

    return (
        jsonify(
            {
                "success": False,
                "error": True,
                "message": result.get("message", "Không thể tạo voucher."),
            }
        ),
        400,
    )


@login_required
@voucher_bp.route("/<int:voucher_id>", methods=["PUT"])
@required
def voucher_edit(voucher_id):
    data = request.get_json()
    print("Request data:", data)

    result = VoucherService.update_voucher(voucher_id, data)
    print("Service result:", result)

    if result.get("success"):
        return (
            jsonify(
                {
                    "success": True,
                    "message": result.get("message", "Voucher updated successfully."),
                    "data": result.get("data"),
                }
            ),
            200,
        )
    else:
        return (
            jsonify(
                {
                    "success": False,
                    "message": result.get("message", "Voucher update failed."),
                    "data": result.get("data"),
                }
            ),
            400,
        )


@login_required
@voucher_bp.route("/<int:voucher_id>", methods=["DELETE"])
@required
def voucher_delete(voucher_id):
    result = VoucherService.delete_voucher(voucher_id)
    if result.get("success"):
        return jsonify({"message": "Voucher deleted successfully"}), 200
    return jsonify({"error": result.get("error")}), 400


@login_required
@voucher_bp.route("/<int:voucher_id>", methods=["GET"])
@required
def get_voucher_by_id(voucher_id):
    voucher = VoucherService.get_voucher_by_id(voucher_id)
    if voucher:
        return jsonify(voucher.to_dict()), 200
    return jsonify({"error": "Voucher not found"}), 404
