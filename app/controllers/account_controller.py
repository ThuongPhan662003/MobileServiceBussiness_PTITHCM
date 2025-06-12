from flask import Blueprint, request, jsonify
from flask_login import login_required
from app.utils.decorator import required
from app.services.account_service import AccountService


account_bp = Blueprint("account", __name__, url_prefix="/accounts")


@login_required
@account_bp.route("/", methods=["GET"])
@required
def get_all_accounts():
    accounts = AccountService.get_all_accounts()
    print(accounts)
    return jsonify(accounts), 200


@login_required
@account_bp.route("/<int:account_id>", methods=["GET"])
@required
def get_account_by_id(account_id):
    account = AccountService.get_account_by_id(account_id)
    if account:
        return jsonify(account.to_dict()), 200
    return jsonify({"error": "Account not found"}), 404


@login_required
@account_bp.route("/", methods=["POST"])
@required
def create_account():
    data = request.get_json()
    result = AccountService.create_account(data)
    if result.get("success"):
        return jsonify({"message": "Account created successfully"}), 201
    return jsonify({"error": result.get("error")}), 400


@login_required
@account_bp.route("/<int:account_id>", methods=["PUT"])
@required
def update_account(account_id):
    data = request.get_json()
    result = AccountService.update_account(account_id, data)
    if result.get("success"):
        return jsonify({"message": "Account updated successfully"}), 200
    return jsonify({"error": result.get("error")}), 400


@login_required
@account_bp.route("/<int:account_id>", methods=["DELETE"])
@required
def delete_account(account_id):
    result = AccountService.delete_account(account_id)
    if result.get("success"):
        return jsonify({"message": "Account deleted successfully"}), 200
    return jsonify({"error": result.get("error")}), 400
