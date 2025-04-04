from flask import Blueprint, request, jsonify
from app.services.voucher_service import VoucherService

voucher_bp = Blueprint("voucher", __name__, url_prefix="/vouchers")


@voucher_bp.route("/", methods=["GET"])
def get_all_vouchers():
    vouchers = VoucherService.get_all_vouchers()
    return jsonify(vouchers), 200


@voucher_bp.route("/<int:voucher_id>", methods=["GET"])
def get_voucher_by_id(voucher_id):
    voucher = VoucherService.get_voucher_by_id(voucher_id)
    if voucher:
        return jsonify(voucher.to_dict()), 200
    return jsonify({"error": "Voucher not found"}), 404


@voucher_bp.route("/", methods=["POST"])
def create_voucher():
    data = request.get_json()
    result = VoucherService.create_voucher(data)
    if result.get("success"):
        return jsonify({"message": "Voucher created successfully"}), 201
    return jsonify({"error": result.get("error")}), 400


@voucher_bp.route("/<int:voucher_id>", methods=["PUT"])
def update_voucher(voucher_id):
    data = request.get_json()
    result = VoucherService.update_voucher(voucher_id, data)
    if result.get("success"):
        return jsonify({"message": "Voucher updated successfully"}), 200
    return jsonify({"error": result.get("error")}), 400


@voucher_bp.route("/<int:voucher_id>", methods=["DELETE"])
def delete_voucher(voucher_id):
    result = VoucherService.delete_voucher(voucher_id)
    if result.get("success"):
        return jsonify({"message": "Voucher deleted successfully"}), 200
    return jsonify({"error": result.get("error")}), 400
