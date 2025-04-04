from flask import Blueprint, request, jsonify
from app.services.country_service import CountryService

country_bp = Blueprint("country", __name__, url_prefix="/countries")


@country_bp.route("/", methods=["GET"])
def get_all_countries():
    countries = CountryService.get_all_countries()
    return jsonify(countries), 200


@country_bp.route("/<int:country_id>", methods=["GET"])
def get_country_by_id(country_id):
    country = CountryService.get_country_by_id(country_id)
    if country:
        return jsonify(country.to_dict()), 200
    return jsonify({"error": "Country not found"}), 404


@country_bp.route("/", methods=["POST"])
def create_country():
    data = request.get_json()
    result = CountryService.create_country(data)
    if result.get("success"):
        return jsonify({"message": "Country created successfully"}), 201
    return jsonify({"error": result.get("error")}), 400


@country_bp.route("/<int:country_id>", methods=["PUT"])
def update_country(country_id):
    data = request.get_json()
    result = CountryService.update_country(country_id, data)
    if result.get("success"):
        return jsonify({"message": "Country updated successfully"}), 200
    return jsonify({"error": result.get("error")}), 400


@country_bp.route("/<int:country_id>", methods=["DELETE"])
def delete_country(country_id):
    result = CountryService.delete_country(country_id)
    if result.get("success"):
        return jsonify({"message": "Country deleted successfully"}), 200
    return jsonify({"error": result.get("error")}), 400
