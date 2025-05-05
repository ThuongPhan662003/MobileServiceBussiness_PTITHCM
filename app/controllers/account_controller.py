from flask import Blueprint, request, jsonify
from flask_login import login_required
from app.services.account_service import AccountService
from app.utils.decorator import roles_required

account_bp = Blueprint("account", __name__, url_prefix="/accounts")


@account_bp.route("/", methods=["GET"])
@login_required
@roles_required("staff")
def get_all_accounts():
    accounts = AccountService.get_all_accounts()
    print(accounts)
    return jsonify(accounts), 200


@account_bp.route("/<int:account_id>", methods=["GET"])
@login_required
@roles_required("staff")
def get_account_by_id(account_id):
    account = AccountService.get_account_by_id(account_id)
    if account:
        return jsonify(account.to_dict()), 200
    return jsonify({"error": "Account not found"}), 404


@account_bp.route("/", methods=["POST"])
@login_required
@roles_required("staff")
def create_account():
    data = request.get_json()
    result = AccountService.create_account(data)
    if result.get("success"):
        return jsonify({"message": "Account created successfully"}), 201
    return jsonify({"error": result.get("error")}), 400


@account_bp.route("/<int:account_id>", methods=["PUT"])
@login_required
@roles_required("staff")
def update_account(account_id):
    data = request.get_json()
    result = AccountService.update_account(account_id, data)
    if result.get("success"):
        return jsonify({"message": "Account updated successfully"}), 200
    return jsonify({"error": result.get("error")}), 400


@account_bp.route("/<int:account_id>", methods=["DELETE"])
@login_required
@roles_required("staff")
def delete_account(account_id):
    result = AccountService.delete_account(account_id)
    if result.get("success"):
        return jsonify({"message": "Account deleted successfully"}), 200
    return jsonify({"error": result.get("error")}), 400
