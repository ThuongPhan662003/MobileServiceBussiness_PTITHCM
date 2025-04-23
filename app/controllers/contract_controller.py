from datetime import datetime
from flask import Blueprint, render_template, request, jsonify
from app.services.contract_service import ContractService
from app.services.subscriber_service import SubscriberService

contract_bp = Blueprint("contract", __name__, url_prefix="/contracts")


@contract_bp.route("/", methods=["GET"])
def index():
    print("hi")
    return render_template("contracts/contracts.html")


@contract_bp.route("/get-subscribers", methods=["GET"])
def get_all_subscribers():
    subscribers = SubscriberService.get_all_subscribers()
    return jsonify(subscribers), 200


@contract_bp.route("/get-all", methods=["GET"])
def get_all_contracts():
    contracts = ContractService.get_all_contracts()
    return jsonify(contracts), 200


@contract_bp.route("/<int:contract_id>", methods=["GET"])
def get_contract_by_id(contract_id):
    contract = ContractService.get_contract_by_id(contract_id)
    if contract:
        return jsonify(contract.to_dict()), 200
    return jsonify({"error": "Contract not found"}), 404


@contract_bp.route("/", methods=["POST"])
def create_contract():
    data = request.get_json()
    print("---------------------", data)
    data["start_date"] = datetime.strptime(data["start_date"], "%Y-%m-%d").date()
    data["end_date"] = (
        datetime.strptime(data["end_date"], "%Y-%m-%d").date()
        if data["end_date"]
        else None
    )
    result = ContractService.create_contract(data)
    if result.get("success"):
        return jsonify({"message": "Contract created successfully"}), 201
    return jsonify({"error": result.get("error")}), 400


@contract_bp.route("/<int:contract_id>", methods=["PUT"])
def update_contract(contract_id):
    data = request.get_json()
    result = ContractService.update_contract(contract_id, data)
    if result.get("success"):
        return jsonify({"message": "Contract updated successfully"}), 200
    return jsonify({"error": result.get("error")}), 400


@contract_bp.route("/<int:contract_id>", methods=["DELETE"])
def delete_contract(contract_id):
    result = ContractService.delete_contract(contract_id)
    if result.get("success"):
        return jsonify({"message": "Contract deleted successfully"}), 200
    return jsonify({"error": result.get("error")}), 400
