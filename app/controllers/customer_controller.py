from flask import Blueprint, request, jsonify, render_template
from app.services.customer_service import CustomerService

customer_bp = Blueprint("customer", __name__, url_prefix="/customers")


@customer_bp.route("/", methods=["GET"])
def get_all_customers():
    customers = CustomerService.get_all_customers()
    return render_template("customers/customer.html", customers=customers)

@customer_bp.route("/<int:id>", methods=["GET"])
def get_customer_by_id(id):
    customer = CustomerService.get_customer_by_id(id)
    if customer:
        return jsonify(customer.to_dict()), 200
    return jsonify({"error": "Customer not found"}), 404

@customer_bp.route("/", methods=["POST"])
def create_customer():
    data = request.get_json()
    result = CustomerService.create_customer(data)
    if result.get("success"):
        return jsonify({"message": "Customer created successfully"}), 201
    return jsonify({"error": result.get("error")}), 400


@customer_bp.route("/<int:customer_id>", methods=["PUT"])
def update_customer(customer_id):
    data = request.get_json()
    result = CustomerService.update_customer(customer_id, data)
    if result.get("success"):
        return jsonify({"message": "Customer updated successfully"}), 200
    return jsonify({"error": result.get("error")}), 400


@customer_bp.route("/<int:customer_id>", methods=["DELETE"])
def delete_customer(customer_id):
    result = CustomerService.delete_customer(customer_id)
    if result.get("success"):
        return jsonify({"message": "Customer deleted successfully"}), 200
    return jsonify({"error": result.get("error")}), 400
