from flask import Blueprint, request, jsonify
from app.services.function_service import FunctionService
from flask_login import login_required
from app.utils.decorator import required

function_bp = Blueprint("function", __name__, url_prefix="/functions")


@login_required
@function_bp.route("/", methods=["GET"])
@required
def get_all_functions():
    functions = FunctionService.get_all_functions()
    return jsonify(functions), 200


@login_required
@function_bp.route("/<int:function_id>", methods=["GET"])
@required
def get_function_by_id(function_id):
    function = FunctionService.get_function_by_id(function_id)
    if function:
        return jsonify(function.to_dict()), 200
    return jsonify({"error": "Function not found"}), 404


@login_required
@function_bp.route("/", methods=["POST"])
@required
def create_function():
    data = request.get_json()
    result = FunctionService.create_function(data)
    if result.get("success"):
        return jsonify({"message": "Function created successfully"}), 201
    return jsonify({"error": result.get("error")}), 400


@login_required
@function_bp.route("/<int:function_id>", methods=["PUT"])
@required
def update_function(function_id):
    data = request.get_json()
    result = FunctionService.update_function(function_id, data)
    if result.get("success"):
        return jsonify({"message": "Function updated successfully"}), 200
    return jsonify({"error": result.get("error")}), 400


@login_required
@function_bp.route("/<int:function_id>", methods=["DELETE"])
@required
def delete_function(function_id):
    result = FunctionService.delete_function(function_id)
    if result.get("success"):
        return jsonify({"message": "Function deleted successfully"}), 200
    return jsonify({"error": result.get("error")}), 400
