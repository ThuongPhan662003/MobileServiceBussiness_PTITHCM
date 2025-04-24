from flask import Blueprint, render_template, request, jsonify

from flask_login import current_user
from app.services.staff_service import StaffService

from app.services.voucher_service import VoucherService

voucher_bp = Blueprint("voucher", __name__, url_prefix="/vouchers")


@voucher_bp.route("/", methods=["GET"])
def voucher_list():
    all_vouchers = VoucherService.get_all_vouchers()
    print("all_vouchers", all_vouchers)
    return render_template("vouchers/voucher_list.html", vouchers=all_vouchers)


@voucher_bp.route("/", methods=["POST"])
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


@voucher_bp.route("/<int:voucher_id>", methods=["PUT"])
def voucher_edit(voucher_id):
    data = request.get_json()
    result = VoucherService.update_voucher(voucher_id, data)
    if result.get("success"):
        return jsonify({"message": "Voucher updated successfully"}), 200
    return jsonify({"error": result.get("error")}), 400


@voucher_bp.route("/<int:voucher_id>", methods=["DELETE"])
def voucher_delete(voucher_id):
    result = VoucherService.delete_voucher(voucher_id)
    if result.get("success"):
        return jsonify({"message": "Voucher deleted successfully"}), 200
    return jsonify({"error": result.get("error")}), 400


@voucher_bp.route("/<int:voucher_id>", methods=["GET"])
def get_voucher_by_id(voucher_id):
    voucher = VoucherService.get_voucher_by_id(voucher_id)
    if voucher:
        return jsonify(voucher.to_dict()), 200
    return jsonify({"error": "Voucher not found"}), 404
